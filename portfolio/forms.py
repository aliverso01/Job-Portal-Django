from django import forms
from portfolio.models import Portfolio

class PortfolioForm(forms.Form):
    class Meta:
        model = Portfolio
        fields = ['logo_empresa', 
                  'biografia', 
                  'profissao', 
                  'especialidade', 
                  'ferramentas', 
                  'idiomas', 
                  'arquivo', 
                  'link_video',

                  #redes sociais
                  'facebook',
                  'instagram',
                  'linkedin',
                  'twitter',
                  'youtube',  

                  #estilzação

                  'background_color',
                  'button_color',
                  'text_color',
                  'font_size',
                  'font_family',
                  'border_radius'
                  ]