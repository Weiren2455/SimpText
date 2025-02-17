import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QPlainTextEdit, QAction, QMessageBox
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat
from PyQt5.QtCore import Qt, QRegExp

# 語法高亮類別 (這裡以 Python 為例)
class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)
        self.highlightingRules = []
        
        # 設定關鍵字格式
        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(Qt.darkBlue)
        keywordFormat.setFontWeight(QFont.Bold)
        keywords = ["def", "class", "if", "else", "elif", "while", "for", "in", "import", "from", "return"]
        for word in keywords:
            pattern = QRegExp("\\b" + word + "\\b")
            self.highlightingRules.append((pattern, keywordFormat))
        
        # 設定單行註解格式
        self.commentFormat = QTextCharFormat()
        self.commentFormat.setForeground(Qt.darkGreen)
        self.commentStartExpression = QRegExp("#")
        
    def highlightBlock(self, text):
        # 套用關鍵字格式
        for pattern, fmt in self.highlightingRules:
            index = pattern.indexIn(text)
            while index >= 0:
                length = pattern.matchedLength()
                self.setFormat(index, length, fmt)
                index = pattern.indexIn(text, index + length)
        
        # 套用註解格式
        index = self.commentStartExpression.indexIn(text)
        if index >= 0:
            length = len(text) - index
            self.setFormat(index, length, self.commentFormat)

# 主編輯器視窗
class CodeEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.currentFile = None
        self.initUI()
        
    def initUI(self):
        # 使用 QPlainTextEdit 作為主要編輯區域
        self.textEdit = QPlainTextEdit()
        self.textEdit.setFont(QFont("Consolas", 12))
        self.setCentralWidget(self.textEdit)
        
        # 初始化語法高亮
        self.highlighter = Highlighter(self.textEdit.document())
        
        # 建立選單
        self.createMenus()
        
        # 設定視窗基本屬性
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('SimpText')
        self.show()
        
    def createMenus(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&檔案')
        
        # 開啟檔案
        openAct = QAction('&開啟', self)
        openAct.setShortcut('Ctrl+O')
        openAct.triggered.connect(self.openFile)
        fileMenu.addAction(openAct)
        
        # 儲存檔案
        saveAct = QAction('&儲存', self)
        saveAct.setShortcut('Ctrl+S')
        saveAct.triggered.connect(self.saveFile)
        fileMenu.addAction(saveAct)
        
        # 另存新檔
        saveAsAct = QAction('另存為', self)
        saveAsAct.triggered.connect(self.saveFileAs)
        fileMenu.addAction(saveAsAct)
        
        # 離開程式
        exitAct = QAction('離開', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(self.close)
        fileMenu.addAction(exitAct)
    
    def openFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "開啟檔案", "", "所有檔案 (*);;Python 檔案 (*.py)", options=options)
        if fileName:
            try:
                with open(fileName, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.textEdit.setPlainText(content)
                self.currentFile = fileName
                self.setWindowTitle(f'SimpText - {fileName}')
            except Exception as e:
                QMessageBox.warning(self, '錯誤', f'無法開啟檔案: {e}')
    
    def saveFile(self):
        if self.currentFile:
            try:
                with open(self.currentFile, 'w', encoding='utf-8') as f:
                    content = self.textEdit.toPlainText()
                    f.write(content)
                QMessageBox.information(self, '訊息', '檔案儲存成功')
            except Exception as e:
                QMessageBox.warning(self, '錯誤', f'無法儲存檔案: {e}')
        else:
            self.saveFileAs()
    
    def saveFileAs(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "另存檔案", "", "所有檔案 (*);;Python 檔案 (*.py)", options=options)
        if fileName:
            self.currentFile = fileName
            self.saveFile()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = CodeEditor()
    sys.exit(app.exec_())
