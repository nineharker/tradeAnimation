# -*- coding: utf-8 -*-
from maya import cmds, mel
from PySide2 import QtWidgets,QtGui
from ..lib import qt

class HorizontalLine(QtWidgets.QFrame):
    #水平のライン
    def __init__(self, *args, **kwargs):
        super(HorizontalLine, self).__init__(*args, **kwargs)
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)

#MainUI
class OptionWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(OptionWidget, self).__init__(*args, **kwargs)

        #GUIの見た目処理　フォームレイアウトをつくる
        mainLayout = QtWidgets.QFormLayout(self)
        horizontalLine = HorizontalLine()


        Label = QtWidgets.QLabel(u"選択した二つのオブジェクトのモーションを入れ替えます\
                                    \nアトリビュートを選択してください")
        mainLayout.addWidget(Label)
        # TradeAnimationのチェックボックス作成
        self.tradeTranslateXcheck = QtWidgets.QCheckBox('translateX')
        self.tradeTranslateXcheck.toggle()
        self.tradeTranslateYcheck = QtWidgets.QCheckBox('translateY')
        self.tradeTranslateYcheck.toggle()
        self.tradeTranslateZcheck = QtWidgets.QCheckBox('translateZ')
        self.tradeTranslateZcheck.toggle()
        acrossLayout = QtWidgets.QHBoxLayout(self)
        acrossLayout.addWidget(self.tradeTranslateXcheck, True)
        acrossLayout.addWidget(self.tradeTranslateYcheck, True)
        acrossLayout.addWidget(self.tradeTranslateZcheck, True)
        mainLayout.addRow('', acrossLayout)
        self.tradeRotateXcheck = QtWidgets.QCheckBox('rotateX')
        self.tradeRotateXcheck.toggle()
        self.tradeRotateYcheck = QtWidgets.QCheckBox('rotateY')
        self.tradeRotateYcheck.toggle()
        self.tradeRotateZcheck = QtWidgets.QCheckBox('rotateZ')
        self.tradeRotateZcheck.toggle()
        acrossLayout = QtWidgets.QHBoxLayout(self)
        acrossLayout.addWidget(self.tradeRotateXcheck, True)
        acrossLayout.addWidget(self.tradeRotateYcheck, True)
        acrossLayout.addWidget(self.tradeRotateZcheck, True)
        mainLayout.addRow('', acrossLayout)

        self.tradeAnimationButton = QtWidgets.QPushButton('TradeMotion')
        mainLayout.addRow('', self.tradeAnimationButton)
        mainLayout.addRow(horizontalLine)

        Label = QtWidgets.QLabel(u"選択したオブジェクトのモーションを反転します\
                                    \nアトリビュートを選択してください")
        mainLayout.addWidget(Label)
        # FlipAnimationのチェックボックス作成
        self.flipTranslateXcheck = QtWidgets.QCheckBox('translateX')
        self.flipTranslateYcheck = QtWidgets.QCheckBox('translateY')
        self.flipTranslateZcheck = QtWidgets.QCheckBox('translateZ')
        acrossLayout = QtWidgets.QHBoxLayout(self)
        acrossLayout.addWidget(self.flipTranslateXcheck, True)
        acrossLayout.addWidget(self.flipTranslateYcheck, True)
        acrossLayout.addWidget(self.flipTranslateZcheck, True)
        mainLayout.addRow('', acrossLayout)
        self.flipRotateXcheck = QtWidgets.QCheckBox('rotateX')
        self.flipRotateYcheck = QtWidgets.QCheckBox('rotateY')
        self.flipRotateYcheck.toggle()
        self.flipRotateZcheck = QtWidgets.QCheckBox('rotateZ')
        self.flipRotateZcheck.toggle()
        acrossLayout = QtWidgets.QHBoxLayout(self)
        acrossLayout.addWidget(self.flipRotateXcheck, True)
        acrossLayout.addWidget(self.flipRotateYcheck, True)
        acrossLayout.addWidget(self.flipRotateZcheck, True)
        mainLayout.addRow('', acrossLayout)

        self.flipAnimationButton = QtWidgets.QPushButton('FlipMotion')
        mainLayout.addRow('', self.flipAnimationButton)

        self.setSignals()

    def setSignals(self):
        #シグナル。メソッドとボタンを関連付け
        self.tradeAnimationButton.clicked.connect(qt.Callback(self.tradeAnimation))
        self.flipAnimationButton.clicked.connect(qt.Callback(self.flipAnimation))

        #//////////////////////ここから実際の処理////////////////////////

    def tradeAnimation(self):
        """
        選択した二つのオブジェクトの、チェックボックスを入れたアトリビュートの
        アニメーションを入れ替えます
        """
        nodes = cmds.ls(sl=True)
        if not len(nodes) == 2:
            return

        # attribute = ["translateX","translateY","translateZ","rotateX","rotateY","rotateZ"]
        attribute = []

        if self.tradeTranslateXcheck.checkState():
            attribute.append("translateX")
        if self.tradeTranslateYcheck.checkState():
            attribute.append("translateY")
        if self.tradeTranslateZcheck.checkState():
            attribute.append("translateZ")
        if self.tradeRotateXcheck.checkState():
            attribute.append("rotateX")
        if self.tradeRotateYcheck.checkState():
            attribute.append("rotateY")
        if self.tradeRotateZcheck.checkState():
            attribute.append("rotateZ")

        if not attribute:
            return

        temp1 = cmds.createNode( 'transform', n='temp1' )
        temp2 = cmds.createNode( 'transform', n='temp2' )
        firstNode = nodes[0]
        secondNode = nodes[1]
        # cmds.copyKey(nodes[0],time=":",at=["translateX", "translateY", "translateZ"],
        #             an="keys",option='curve',float=":",shape=True,cp=False)
        # attribute = ["rotateX","rotateY","rotateZ"]
        # attribute = ["translateX","translateY","translateZ"]


        cmds.copyKey(firstNode,at=attribute,option="curve")
        cmds.pasteKey(temp1,at=attribute)

        cmds.copyKey(secondNode,at=attribute,option="curve")
        cmds.pasteKey(temp2,at=attribute)

        cmds.copyKey(temp1,at=attribute,option="curve")
        cmds.pasteKey(secondNode,o="replaceCompletely",at=attribute)

        cmds.copyKey(temp2,at=attribute,option="curve")
        cmds.pasteKey(firstNode,o="replaceCompletely",at=attribute)

        cmds.delete(temp1)
        cmds.delete(temp2)

        cmds.select(nodes)

    def flipAnimation(self):
        """
        選択したオブジェクトのアニメーションを反転します
        チェックボックスを入れたアトリビュートのアニメーションカーブ-1をかける
        """
        nodes = cmds.ls(sl=True)
        node = nodes[0]
        if not nodes:
            return
        attribute = []
        if self.flipTranslateXcheck.checkState():
            attribute.append("translateX")
        if self.flipTranslateYcheck.checkState():
            attribute.append("translateY")
        if self.flipTranslateZcheck.checkState():
            attribute.append("translateZ")
        if self.flipRotateXcheck.checkState():
            attribute.append("rotateX")
        if self.flipRotateYcheck.checkState():
            attribute.append("rotateY")
        if self.flipRotateZcheck.checkState():
            attribute.append("rotateZ")
            # アトリビュートが選択されてなかったら終了
        if not attribute:
            return

        cmds.scaleKey(node,at=attribute,valueScale = -1)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('TradeAnimation')
        self.resize(300, 200)

        widget = OptionWidget()
        self.setCentralWidget(widget)

    def show(self):
    #ウィンドウズが最小か最大のときオーバーライドする
        if self.isMinimized() or self.isMaximized():
            self.showNormal()
        else:
            super(MainWindow,self).show()



def main():
    app = MainWindow(qt.getMayaWindow())
    app.show()
