import math
import qt

class AnimatedProgressBar(qt.QProgressBar):
    navigationChanged = qt.Signal(str)
    def __init__(self, colors=None, minimum_height=0, minimum_width=0, background_color=qt.Qt.white, border_color=qt.Qt.black):
        super().__init__()
        self.minimumHeight = minimum_height
        self.minimumWidth = minimum_width
        self.animation_timer = qt.QTimer(self)
        self.background_color = background_color
        self.border_color = border_color

        if not colors or len(colors) != 2 or not isinstance(colors[0], qt.QColor) or not isinstance(colors[1], qt.QColor):
            self.animation_colors = [
                qt.QColor(0, 255, 255),
                qt.QColor(255, 0, 255)
            ]
        else:
            self.animation_colors = colors

        self.animation_index = 0
        self.animation_direction = qt.QVariantAnimation.Forward

        self.animation = qt.QVariantAnimation()
        self.animation.valueChanged.connect(self.animationValueChanged)
        self.animation.finished.connect(self.animationFinished)
        self.animation.setDuration(2000)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation_timer.singleShot(0, self.startAnimation)

    def startAnimation(self):
        if self.animation_direction == qt.QVariantAnimation.Forward:
            self.animation_index = 1
            self.animation_direction = qt.QVariantAnimation.Backward
        else:
            self.animation_index = 0
            self.animation_direction = qt.QVariantAnimation.Forward
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setDuration(1000)
        self.animation.start()

    def animationValueChanged(self, value):
        self.update()

    def animationFinished(self):
        self.startAnimation()

    def paintEvent(self, event):
        bar_height = self.height
        bar_width = self.width

        painter = qt.QPainter(self)
        painter.setRenderHint(qt.QPainter.Antialiasing)

        border_color = self.border_color
        painter.setBrush(self.background_color)
        painter.setPen(qt.QPen(border_color, 1))
        painter.drawRoundedRect(0, 0, bar_width, bar_height, bar_height / 2, bar_height / 2)

        filled_width = int(bar_width * (self.value / self.maximum))
        start_color = self.animation_colors[self.animation_index]
        end_color = self.animation_colors[(self.animation_index + 1) % len(self.animation_colors)]

        color = qt.QColor()
        color.setRedF(start_color.redF() + (end_color.redF() - start_color.redF()) * self.animation.currentValue)
        color.setGreenF(start_color.greenF() + (end_color.greenF() - start_color.greenF()) * self.animation.currentValue)
        color.setBlueF(start_color.blueF() + (end_color.blueF() - start_color.blueF()) * self.animation.currentValue)

        brush = qt.QBrush(color)

        painter.setBrush(brush)
        painter.drawRoundedRect(0, 0, filled_width, bar_height, bar_height / 2, bar_height / 2)

        stripe_width = 10
        stripe_spacing = 25
        num_stripes = math.ceil(filled_width-stripe_width / stripe_spacing)

        stripe_path = qt.QPainterPath()
        stripe_path.moveTo(1, bar_height-1)
        stripe_path.lineTo(stripe_width-1, 1)

        painter.setTransform(qt.QTransform().translate(-self.animation.currentValue * stripe_spacing, 0))

        painter.setPen(qt.QPen(self.background_color, stripe_width))

        for i in range(num_stripes):
            stripe_x = i * stripe_spacing
            painter.drawPath(stripe_path.translated(stripe_x, 0))

        painter.setTransform(qt.QTransform().translate(0, 0))
        painter.setBrush(qt.QBrush(qt.Qt.transparent))
        painter.setPen(qt.QPen(border_color, 1.25))
        painter.drawRoundedRect(0, 0, filled_width, bar_height, bar_height / 2, bar_height / 2)
        painter.drawRoundedRect(0, 0, bar_width, bar_height, bar_height / 2, bar_height / 2)
