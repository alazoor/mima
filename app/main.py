
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

class OCRApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15
        
        # خلفية التطبيق
        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        # عنوان التطبيق
        title_label = Label(
            text='[b][color=#2E7D32]تطبيق التعرف على النص العربي[/color][/b]',
            markup=True,
            size_hint=(1, 0.15),
            font_size='28sp',
            halign='center'
        )
        self.add_widget(title_label)
        
        # صورة رمزية
        self.image_widget = Image(
            source='assets/icon.png',
            size_hint=(1, 0.3),
            allow_stretch=True
        )
        self.add_widget(self.image_widget)
        
        # منطقة النتائج
        self.results_text = Label(
            text='انقر على الزر لبدء التعرف على النص',
            size_hint=(1, 0.4),
            font_size='18sp',
            text_size=(None, None),
            halign='center',
            valign='middle'
        )
        self.add_widget(self.results_text)
        
        # أزرار التحكم
        buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.15), spacing=10)
        
        self.ocr_btn = Button(
            text='تشغيل OCR',
            size_hint=(0.5, 1),
            background_color=(0.2, 0.6, 0.8, 1),
            font_size='18sp'
        )
        self.ocr_btn.bind(on_press=self.run_ocr)
        buttons_layout.add_widget(self.ocr_btn)
        
        self.clear_btn = Button(
            text='مسح النتائج',
            size_hint=(0.5, 1),
            background_color=(0.8, 0.3, 0.3, 1),
            font_size='18sp'
        )
        self.clear_btn.bind(on_press=self.clear_results)
        buttons_layout.add_widget(self.clear_btn)
        
        self.add_widget(buttons_layout)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def run_ocr(self, instance):
        self.results_text.text = 'جاري التعرف على النص...'
        self.ocr_btn.disabled = True
        self.clear_btn.disabled = True
        
        # محاكاة عملية OCR
        Clock.schedule_once(self.process_ocr, 2)

    def process_ocr(self, dt):
        sample_text = 'مرحباً بك في تطبيق OCR\nهذا تطبيق تجريبي للتعرف على النص العربي\nيمكنك إضافة وظيفة OCR الحقيقية هنا'
        
        self.results_text.text = sample_text
        self.ocr_btn.disabled = False
        self.clear_btn.disabled = False

    def clear_results(self, instance):
        self.results_text.text = 'انقر على الزر لبدء التعرف على النص'

class ArabicOCRApp(App):
    def build(self):
        self.title = 'تطبيق OCR العربي'
        return OCRApp()

if __name__ == '__main__':
    ArabicOCRApp().run()
