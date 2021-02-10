import QtQuick 2.15
import QtQuick.Controls 2.15
import Qt.labs.qmlmodels 1.0
import QtGraphicalEffects 1.15


Item {
    width: 366
    height: 598

    Connections{
        target: funcsAjustePage
        function onFillParamsTable(param, value, uncertainty){
            tableParamsModel.appendRow({"Parâmetros" : param, "Valor": value, "Incerteza" : uncertainty})
        }

        function onWriteInfos(expr){
            infos.text = expr
        }
    }

    // Functions
    QtObject{
        id: internal1

        function clearTableParams(){
            tableParamsModel.clear()
            tableParamsModel.rows = [
                        {
                            "Parâmetros": "Parâmetros",
                            "Valor": "Valor",
                            "Incerteza": "Incerteza",
                        }
                    ]
        }
    }

    Rectangle {
        id: bg
        color: "#565e66"
        anchors.fill: parent

        Rectangle {
            id: rectangle1
            height: 50
            color: "#00000000"
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.rightMargin: 0
            anchors.leftMargin: 0
            anchors.topMargin: 0

            Label {
                id: label
                x: 10
                y: 274
                width: 110
                height: 49
                color: "#ffffff"
                text: qsTr("Expressão | y(x) = ")
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.left
                verticalAlignment: Text.AlignVCenter
                font.pointSize: 10
                anchors.leftMargin: 10
            }

            TextField {
                id: expression
                text: ""
                anchors.left: label.right
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.rightMargin: 10
                anchors.topMargin: 10
                anchors.bottomMargin: 10
                anchors.leftMargin: 5
                placeholderText: qsTr("")
                selectByMouse: true
            }
        }

        Frame {
            id: frame
            height: 130
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: rectangle.bottom
            anchors.topMargin: 10
            anchors.rightMargin: 10
            anchors.leftMargin: 10

            TableView {
                id: tableParams
                anchors.fill: parent
                anchors.rightMargin: 5
                interactive: false
                columnSpacing: 1
                rowSpacing: 0.8
                clip: true
                boundsBehavior: Flickable.DragOverBounds

                ScrollBar.vertical: ScrollBar{
                    id: scrollBarTableData
                    policy: ScrollBar.AlwaysOn
                    parent: tableParams.parent
                    anchors.top: tableParams.top
                    anchors.left: tableParams.right
                    anchors.bottom: tableParams.bottom
                }

                model: TableModel {

                    id: tableParamsModel

                    TableModelColumn { display: "Parâmetros" }
                    TableModelColumn { display: "Valor" }
                    TableModelColumn { display: "Incerteza" }

                    rows: [
                        {
                            "Parâmetros": "Parâmetros",
                            "Valor": "Valor",
                            "Incerteza": "Incerteza",
                        }
                    ]
                }

                delegate: Rectangle {
                    height: 200
                    implicitWidth: tableParams.width/3
                    implicitHeight: 20
                    border.width: 1

                    Text {
                        text: display
                        anchors.centerIn: parent
                    }
                }
            }
        }

        GroupBox {
            id: groupBox
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: frame.bottom
            anchors.bottom: parent.bottom
            anchors.leftMargin: 10
            anchors.rightMargin: 10
            anchors.bottomMargin: 50
            anchors.topMargin: 10
            title: qsTr("Dados do Ajuste")

            label: Label {
                x: groupBox.leftPadding
                width: groupBox.availableWidth
                text: groupBox.title
                color: "#ffffff"
                elide: Text.ElideRight
            }

            TextEdit {
                id: infos
                color: "#ffffff"
                text: ""
                anchors.fill: parent
                font.pointSize: 10
                activeFocusOnPress: false
                cursorVisible: false
                readOnly: true
                selectByMouse: true
            }

        }

        Button {
            id: btnPlot
            text: qsTr("Plot")
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: groupBox.bottom
            anchors.bottom: parent.bottom
            font.pointSize: 10
            font.bold: false
            anchors.bottomMargin: 10
            anchors.topMargin: 10
            anchors.rightMargin: 10
            anchors.leftMargin: 10

            onClicked:{
                internal1.clearTableParams()
                funcsAjustePage.loadExpression(expression.text, p0.text)
            }

            QtObject{
                id: internal
                property var dynamicColor: if(btnPlot.down){
                                               btnPlot.down ? "#00a1f1" : "#34334a"
                                           } else {
                                               btnPlot.hovered ? "#23272E" : "#34334a"
                                           }

            }

            background: Rectangle{
                id: btnbg
                radius: 10
                color: internal.dynamicColor
            }

            contentItem: Item{
                anchors.fill: parent
                id: content

                Text{
                    color: "#ffffff"
                    text: "Plot"
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                }
            }
        }

        Rectangle {
            id: rectangle
            height: 50
            color: "#00000000"
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: rectangle1.bottom
            anchors.topMargin: 10
            anchors.leftMargin: 0
            anchors.rightMargin: 0

            Label {
                id: label1
                x: 10
                y: 274
                width: 110
                height: 49
                color: "#ffffff"
                text: qsTr("Parâmetros Iniciais")
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.left
                verticalAlignment: Text.AlignVCenter
                anchors.leftMargin: 10
                font.pointSize: 10
            }

            TextField {
                id: p0
                anchors.left: label1.right
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.leftMargin: 5
                anchors.topMargin: 10
                placeholderText: qsTr("")
                anchors.rightMargin: 10
                anchors.bottomMargin: 10
                selectByMouse: true
            }
        }
    }
}

/*##^##
Designer {
    D{i:0;height:720;width:600}D{i:15}
}
##^##*/
