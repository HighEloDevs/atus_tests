import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15
import QtQuick.Dialogs 1.3
import QtQuick.Layouts 1.11
import "../colors.js" as Colors
import "../controls"

Popup {
    id: root
    anchors.centerIn: Overlay.overlay
    closePolicy: Popup.CloseOnEscape
    modal: true
    focus: true
    leftInset: 0
    rightInset: 0
    bottomInset: 0
    topInset: 0
    margins: 5

    property var kargs: ({
        alpha: alpha.text,          
        label:label.checked,       
        hatch:hatch.currentText,
        fill:fill.checked,        
        fc:String(fc.primaryColor),     
        lw:lw.value,            
        ec:String(ec.primaryColor),     
    })

    function setData(data){
        alpha.text = data["alpha"]
        label.checked = data["alpha"]
        hatch.currentIndex = hatch.find(data["hatch"])
        fill.checked = data["fill"]
        fc.primaryColor = data["fc"]
        lw.value = data["lw"]
        ec.primaryColor = data["ec"]
    }

    background: Rectangle{
        id: bg
        anchors.fill: parent
        radius: 10
        opacity: 0.95
        color: Colors.color2 
        border.width: 2
        border.color: "#fff"
        LinearGradient{
            end: Qt.point(bg.width, bg.height)
            gradient: Gradient{
                GradientStop{
                    position: 0
                    color: Colors.color2 + "80"
                }
                GradientStop{
                    position: 1
                    color: "#202020"
                }
            }
            source: bg
            start: Qt.point(0, 0)
            anchors.fill: parent
            anchors.margins: 2
            smooth: true
        }

        IconButton{
            anchors.right: parent.right
            anchors.rightMargin: -width/3
            anchors.top: parent.top
            anchors.topMargin: -width/3
            width: 30
            height: 30
            r: 20
            z: 1
            primaryColor: Colors.color1
            hoverColor: Colors.color1
            clickColor: Colors.color3
            iconColor: '#fff'
            iconUrl: '../../images/icons/close-24px.svg'
            iconWidth: 20
            borderWidth: 2
            borderColor: "#fff"

            onClicked: root.close()
        }

        ColumnLayout{
            anchors.fill: parent
            spacing: 5
            Text{
                id: popupTitle
                Layout.fillWidth: true
                Layout.topMargin: 20
                Layout.alignment: Qt.AlignHCenter
                text: "Configurações do conjunto de dados" 
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.bold: true
                font.pointSize: 14
                color: "#fff"
            }

            GridLayout{
                Layout.margins: 10
                Layout.fillWidth: true
                Layout.fillHeight: true
                columns: 12
                rows: 20

                TextInputCustom{
                    id: alpha
                    Layout.columnSpan: 6
                    Layout.fillWidth: true
                    focusColor: Colors.mainColor2
                    title: 'Opacidade'
                    textHolder: 'Opacidade das barras. Ex.: 0.9, 0.32'
                    defaultColor: '#fff'
                    textColor: '#fff'
                    validator: RegExpValidator{regExp: /^[0]+([\.]?[0-9]+)?$/}
                }

                CheckBoxCustom{
                    id: label
                    Layout.columnSpan: 6
                    Layout.alignment: Qt.AlignCenter
                    checked: false
                    texto: "Contagens em cima"
                    w: 22
                }

                ComboBoxCustom{
                    id: hatch
                    Layout.columnSpan: 4
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignCenter
                    highlightColor: Colors.mainColor2
                    label: "Textura"
                    model: ["", "/", "\\", "|", "-", "+", "x", "o", "O", ".", "*"]
                }

                CheckBoxCustom{
                    id: fill
                    Layout.columnSpan: 4
                    Layout.alignment: Qt.AlignCenter
                    checked: false
                    texto: "Preencher barras"
                    w: 22
                }

                TextButton{ 
                    id: fc
                    Layout.columnSpan: 4
                    height: 20
                    width: 60
                    radius: 10
                    primaryColor: "#006e00"
                    clickColor: primaryColor
                    hoverColor: primaryColor
                    texto: "Cor das barras"
                    textColor: "#fff"
                    ColorDialog {
                            id: colorDialog1
                            title: "Escolher cor para as bordas das barras"
                            onAccepted: {
                                fc.primaryColor = String(colorDialog1.color)
                            }
                        }
                    onClicked: colorDialog1.open()
                }

                Text{
                    Layout.columnSpan: 4
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter
                    text: "Espessura da borda" 
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    font.bold: true
                    font.pointSize: 8
                    color: "#fff"
                }

                SpinBox {
                    id: lw
                    Layout.columnSpan: 4
                    Layout.preferredHeight: 30
                    value: 2
                    wrap: false
                    stepSize: 1
                    to: 10
                    from: 1
                }

                TextButton{
                    id: ec
                    Layout.columnSpan: 4
                    height: 20
                    width: 60
                    radius: 10
                    primaryColor: "#006e00"
                    clickColor: primaryColor
                    hoverColor: primaryColor
                    texto: "Cor das bordas"
                    textColor: "#fff"
                    ColorDialog {
                            id: colorDialog2
                            title: "Escolher cor para as bordas das barras"
                            onAccepted: {
                                ec.primaryColor = String(colorDialog2.color)
                            }
                        }
                    onClicked: colorDialog2.open()
                }
            }
        }
    }
}