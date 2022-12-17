from django import forms


class CustomCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    template_name = 'hololiveRankingApp/widgets/custom_checkbox.html'
    option_template_name = 'hololiveRankingApp/widgets/custom_checkbox_option.html'

    def __init__(self, attrs=None):
        super().__init__(attrs)
        if 'class' in self.attrs:
            self.attrs['class'] += ' tag_box_choice'
        else:
            self.attrs['class'] = 'tag_box_choice'