import os
import sys
from functools import partial

from PySide6.QtWidgets import (QApplication, QWizard, QFileDialog, QMessageBox)
from PySide6.QtCore import Qt, QThread, Signal

from pyfemtet_opt_gui.ui.ui_detailed_wizard import Ui_DetailedWizard

from pyfemtet_opt_gui.item_as_model import MyStandardItemAsTableModelWithoutHeader
from pyfemtet_opt_gui.problem_model import ProblemItemModel, CustomProxyModel
from pyfemtet_opt_gui.obj_model import ObjTableDelegate

from pyfemtet_opt_gui.script_builder import build_script_main

from pyfemtet_opt_gui.ui.return_code import ReturnCode, should_stop

import pyfemtet_opt_gui._p as _p  # must be same folder and cannot import via `from` keyword.


# noinspection PyMethodMayBeStatic
class MainWizard(QWizard):

    def __init__(self, problem: ProblemItemModel, parent=None):
        super().__init__(parent=parent)
        self._problem: ProblemItemModel = problem
        self.worker = OptimizationWorker()
        self.worker.finished.connect(self.optimization_finished)

    def set_ui(self, ui):
        # noinspection PyAttributeOutsideInit
        self._ui = ui

        # set optimization settings
        model = self._problem.run_model
        proxy_model = MyStandardItemAsTableModelWithoutHeader(model)
        proxy_model.setSourceModel(model)
        self._ui.tableView_run.setModel(proxy_model)

        # disable next button if checker returns False
        self._ui.wizardPage1_launch.isComplete = self.check_femtet_alive
        self._ui.wizardPage2_model.isComplete = partial(self.check_femprj_valid, show_warning=False)
        self._ui.wizardPage3_param.isComplete = partial(self.check_prm_used_any, show_warning=False)
        self._ui.wizardPage4_obj.isComplete = partial(self.check_obj_used_any, show_warning=False)
        # self._ui.wizardPage6_run.isComplete =  # currently, FEMOpt.optimize() requires no arguments.

        # connect dataChanged to completeChanged(=emit isComplete)
        for page_id in self.pageIds():
            page = self.page(page_id)
            self._problem.dataChanged.connect(page.completeChanged)

        # show warning if finish during optimization
        def validate_finish() -> bool:
            out = True
            if self.worker.running:
                ret = QMessageBox.warning(
                    self, 'warning', '最適化の実行中にダイアログを閉じると最適化は強制終了されます。よろしいですか？',
                    QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No
                )
                out = ret == QMessageBox.StandardButton.Yes
            return out
        self._ui.wizardPage9_verify.validatePage = validate_finish

        # running condition warning
        def validate_run_model() -> bool:
            out = True
            # If finish condition is not specified,
            # the optimization process will be an endless loop.
            if len(self._problem.run_model.get_finish_conditions()) == 0:
                ret = QMessageBox.warning(
                    self, 'warning', '終了判定に関わる条件が指定されていないため、生成されるプログラムは手動で停止するまで計算を続けます。よろしいですか？',
                    QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No
                )
                out = ret == QMessageBox.StandardButton.Yes
            return out
        self._ui.wizardPage6_run.validatePage = validate_run_model

    def update_problem(self, _=False, show_warning=True):  # _ is the disposal variable of click() signal.
        return_codes = list()

        return_codes.append(self.load_femprj())
        return_codes.append(self.load_prm())
        return_codes.append(self.load_obj())

        if show_warning:
            for return_code in return_codes:
                if should_stop(return_code):  # show message
                    break  # if error, stop show message

    def load_femprj(self) -> ReturnCode:
        # モデルの再読み込み
        ret_code = self._problem.femprj_model.load()
        prj, model = self._problem.femprj_model.get_femprj()
        self._ui.plainTextEdit_prj.setPlainText(prj)
        self._ui.plainTextEdit_model.setPlainText(model)
        return ret_code

    def load_prm(self) -> ReturnCode:
        # モデルの再読み込み
        ret_code = self._problem.prm_model.load()
        # モデルをビューに再設定
        model = self._problem.prm_model
        proxy_model = MyStandardItemAsTableModelWithoutHeader(model)
        proxy_model.setSourceModel(model)
        self._ui.tableView_prm.setModel(proxy_model)
        return ret_code

    def load_obj(self) -> ReturnCode:
        # モデルの再読み込み
        ret_code = self._problem.obj_model.load()
        # モデルをビューに再設定
        model = self._problem.obj_model
        proxy_model = MyStandardItemAsTableModelWithoutHeader(model)
        proxy_model.setSourceModel(model)
        self._ui.tableView_obj.setModel(proxy_model)
        delegate = ObjTableDelegate(proxy_model)
        self._ui.tableView_obj.setItemDelegate(delegate)
        return ret_code

    def connect_process(self):
        button = self._ui.pushButton_launch

        if len(_p._get_pids('Femtet.exe')) == 0:
            button.setText('Femtet を起動して接続します。\n少し時間がかかります...')
        else:
            button.setText('接続中です...')
        button.setEnabled(False)
        button.repaint()

        if _p.connect_femtet():
            _p.logger.info(f'Connected! (pid: {_p.pid})')  # TODO: show dialog

            # update model
            self.update_problem(show_warning=False)

        button.setText(button.accessibleName())
        button.setEnabled(True)
        button.repaint()

        self._ui.wizardPage1_launch.completeChanged.emit()

    def build_script(self):

        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        dialog.setNameFilter("Python files (*.py)")

        if dialog.exec():
            path = dialog.selectedFiles()[0]
            if not path.endswith('.py'): path += '.py'
            dir_path = os.path.dirname(path)
            if os.path.isdir(dir_path):
                with_run = self._ui.checkBox_save_with_run.checkState() == Qt.CheckState.Checked

                if with_run:
                    self.worker.set(path, self._problem)
                    self.start_optimization()
                else:
                    build_script_main(self._problem, path, False)

            else:
                _p.logger.error('存在しないフォルダのファイルが指定されました。')

    def check_femtet_alive(self):
        alive = _p.check_femtet_alive()

        label = self._ui.label_connectionState
        if alive:
            message = '接続されています。「次へ / Next」を押して下さい。'
            color = '009900'
        else:
            message = '接続されていません。'
            color = 'FF0000'

        text = f"<html><head/><body><p><span style='color:#{color}'>{message}</span></p></body></html>"
        label.setText(text)

        return alive

    def check_save_button_should_enabled(self):
        button = self._ui.pushButton_save_script
        if self.worker.running and self._ui.checkBox_save_with_run.isChecked():
            button.setEnabled(False)  # Disable the button while the function is running
            button.setText('最適化の実行中はスクリプトを保存できません。')
        else:
            button.setEnabled(True)  # Enable the button when the function has finished
            button.setText(button.accessibleName())

    def start_optimization(self):
        self.worker.start()
        self.worker.running = True  # おそらく実行時間の問題で self.run() が走るより先に check が走るので、先に True にしておく。
        self.check_save_button_should_enabled()

    def optimization_finished(self):
        self.check_save_button_should_enabled()

    def check_femprj_valid(self, show_warning=True):
        femprj_model = self._problem.femprj_model
        femprj, model = femprj_model.get_femprj()
        out = False
        if femprj == '':
            out = False
        elif not os.path.exists(femprj):
            out = False
        else:
            out = True
        if show_warning and not out:
            should_stop(ReturnCode.ERROR.FEMTET_NO_PROJECT, parent=self)
        return out

    def check_prm_used_any(self, show_warning=True):
        prm_model = self._problem.prm_model
        col = prm_model.get_col_from_name('use')
        used = []
        for row in range(1, prm_model.rowCount()):
            index = prm_model.createIndex(row, col)
            used.append(prm_model.data(index, Qt.ItemDataRole.CheckStateRole))
        out = any(used)
        if show_warning and not out:
            should_stop(ReturnCode.WARNING.PARAMETER_NOT_SELECTED, parent=self)
        return out

    def check_obj_used_any(self, show_warning=True):
        obj_model = self._problem.obj_model
        col = obj_model.get_col_from_name('use')
        used = []
        for row in range(1, obj_model.rowCount()):
            index = obj_model.createIndex(row, col)
            used.append(obj_model.data(index, Qt.ItemDataRole.CheckStateRole))
        out = any(used)
        if show_warning and not out:
            should_stop(ReturnCode.WARNING.OBJECTIVE_NOT_SELECTED, parent=self)
        return out


class OptimizationWorker(QThread):
    finished = Signal()
    running = False

    def set(self, path, problem):
        self.path = path
        self.problem = problem

    def run(self):  # Override the run method to execute your long-time function
        self.running = True
        build_script_main(self.problem, self.path, True)
        self.running = False
        self.finished.emit()



def main():
    app = QApplication(sys.argv)

    g_problem: ProblemItemModel = ProblemItemModel()

    wizard = MainWizard(g_problem)

    ui_wizard = Ui_DetailedWizard()
    ui_wizard.setupUi(wizard)

    g_proxy_model = CustomProxyModel(g_problem)
    g_proxy_model.setSourceModel(g_problem)
    ui_wizard.treeView.setModel(g_proxy_model)

    wizard.set_ui(ui_wizard)  # ui を登録
    wizard.update_problem(show_warning=False)  # ui へのモデルの登録

    wizard.show()  # ビューの表示
    sys.exit(app.exec())  # アプリケーションの実行


if __name__ == '__main__':
    main()
