import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
import os
import threading

try:
    from rapidocr_onnxruntime import RapidOCR
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

class OCRApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15
        self.ocr_engine = None
        self.current_image_path = None
        
        # خلفية التطبيق
        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        # عنوان التطبيق
        title_label = Label(
            text='[b][color=#2E7D32]تطبيق التعرف على النص العربي[/color][/b]',
            markup=True,
            size_hint=(1, 0.1),
            font_size='24sp',
            halign='center'
        )
        self.add_widget(title_label)
        
        # حالة OCR
        self.status_label = Label(
            text='جاري تحميل محرك OCR...' if OCR_AVAILABLE else 'محرك OCR غير متوفر',
            size_hint=(1, 0.1),
            font_size='16sp'
        )
        self.add_widget(self.status_label)
        
        # صورة معاينة
        self.image_widget = Image(
            size_hint=(1, 0.3),
            allow_stretch=True
        )
        self.add_widget(self.image_widget)
        
        # منطقة النتائج
        self.results_label = Label(
            text='سيظهر النص المعروف هنا...',
            size_hint=(1, 0.3),
            font_size='16sp',
            text_size=(None, None),
            halign='center',
            valign='top'
        )
        self.add_widget(self.results_label)
        
        # أزرار التحكم
        buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)
        
        self.load_btn = Button(
            text='اختر صورة',
            size_hint=(0.5, 1),
            background_color=(0.2, 0.6, 0.8, 1)
        )
        self.load_btn.bind(on_press=self.show_file_chooser)
        buttons_layout.add_widget(self.load_btn)
        
        self.ocr_btn = Button(
            text='تعرف على النص',
            size_hint=(0.5, 1),
            background_color=(0.4, 0.7, 0.4, 1)
        )
        self.ocr_btn.bind(on_press=self.run_ocr)
        buttons_layout.add_widget(self.ocr_btn)
        
        self.add_widget(buttons_layout)
        
        # تهيئة OCR في الخلفية
        if OCR_AVAILABLE:
            Clock.schedule_once(self.init_ocr, 1)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def init_ocr(self, dt):
        try:
            self.status_label.text = 'جاري تحميل نماذج OCR...'
            # استخدام النماذج المدمجة مع RapidOCR
            self.ocr_engine = RapidOCR()
            self.status_label.text = 'محرك OCR جاهز! اختر صورة'
        except Exception as e:
            self.status_label.text = f'خطأ في تحميل OCR: {str(e)}'

    def show_file_chooser(self, instance):
        content = BoxLayout(orientation='vertical')
        filechooser = FileChooserListView()
        content.add_widget(filechooser)
        
        btn_layout = BoxLayout(size_hint_y=None, height=50)
        select_btn = Button(text='اختر')
        cancel_btn = Button(text='إلغاء')
        
        btn_layout.add_widget(select_btn)
        btn_layout.add_widget(cancel_btn)
        content.add_widget(btn_layout)
        
        popup = Popup(title='اختر صورة', content=content, size_hint=(0.9, 0.9))
        
        def select_file(btn):
            if filechooser.selection:
                self.load_image(filechooser.selection[0])
            popup.dismiss()
        
        def cancel(btn):
            popup.dismiss()
        
        select_btn.bind(on_press=select_file)
        cancel_btn.bind(on_press=cancel)
        popup.open()

    def load_image(self, image_path):
        try:
            self.image_widget.source = image_path
            self.image_widget.reload()
            self.current_image_path = image_path
            self.results_label.text = 'الصورة جاهزة للتعرف على النص'
        except Exception as e:
            self.results_label.text = f'خطأ في تحميل الصورة: {str(e)}'

    def run_ocr(self, instance):
        if not self.current_image_path:
            self.results_label.text = 'الرجاء اختيار صورة أولاً'
            return
            
        if not self.ocr_engine:
            self.results_label.text = 'محرك OCR غير جاهز بعد'
            return
            
        self.results_label.text = 'جاري التعرف على النص...'
        self.ocr_btn.disabled = True
        
        # تشغيل OCR في thread منفصل
        threading.Thread(target=self.process_ocr, daemon=True).start()

    def process_ocr(self):
        try:
            result, elapsed = self.ocr_engine(self.current_image_path)
            
            # تحديث الواجهة في thread الرئيسي
            def update_ui():
                if result:
                    text_results = []
                    for line in result:
                        if len(line) >= 2:
                            text_results.append(line[1])
                    
                    if text_results:
                        arabic_text = '\n'.join(text_results)
                        self.results_label.text = f'النص الموجود:\n{arabic_text}'
                    else:
                        self.results_label.text = 'لم يتم العثور على نص'
                else:
                    self.results_label.text = 'لم يتم العثور على نص في الصورة'
                    
                self.ocr_btn.disabled = False
            
            Clock.schedule_once(lambda dt: update_ui(), 0)
            
        except Exception as e:
            def show_error():
                self.results_label.text = f'خطأ في التعرف على النص: {str(e)}'
                self.ocr_btn.disabled = False
            
            Clock.schedule_once(lambda dt: show_error(), 0)

class ArabicOCRApp(App):
    def build(self):
        self.title = 'تطبيق OCR العربي'
        return OCRApp()

if __name__ == '__main__':
    ArabicOCRApp().run()
