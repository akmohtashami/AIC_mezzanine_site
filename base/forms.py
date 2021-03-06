# -*- coding: utf-8 -*-
from base.models import Submit, Team, TeamInvitation, Member
from django import forms
from django.utils.translation import ugettext_lazy as _
from django_countries.widgets import CountrySelectWidget
from game.models import Game
from mezzanine.accounts.forms import ProfileForm as mezzanine_profile_form
from mezzanine.utils.email import send_mail_template


class ProfileForm(mezzanine_profile_form):
    terms = forms.BooleanField(required=True, label=_("Accept Terms"),
                               help_text=_("terms_of_service_text"))

    class Meta:
        model = Member
        fields = (
            "first_name", "last_name", "phone_number", "country", "education_place", "email",
            "username"
        )
        widgets = {'country': CountrySelectWidget()}

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].required = False
        # self.fields['phone_number'].initial = "+989123456789"
        self.fields['education_place'].required = False


class SubmitForm(forms.ModelForm):
    class Meta:
        model = Submit
        fields = ('lang', 'code',)

    def __init__(self, competition, *args, **kwargs):
        super(SubmitForm, self).__init__(*args, **kwargs)
        self.fields['lang'].queryset = competition.supported_langs.all()


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name',)

    def save(self, commit=True, user=None, competition=None):
        instance = super(TeamForm, self).save(commit=False)
        instance.competition = competition
        instance.head = user
        instance.save()
        user.team = instance
        user.save()
        return instance


class TeamNameForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'id')


class InvitationForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        if not Member.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(_('user not found'))
        self.member = Member.objects.get(email=self.cleaned_data['email'])
        return self.cleaned_data['email']

    def save(self, team, host):
        invitation, is_new = TeamInvitation.objects.get_or_create(member=self.member, team=team)
        send_mail_template(_('AIChallenge team invitation'), 'mail/invitation_mail', '',
                           self.member.email, context={'team': team.name,
                                                       'abs_link': invitation.accept_link,
                                                       'current_host': host})


class WillComeForm(forms.ModelForm):
    #
    # def __init__(self, *args, **kwargs):
    #     super(WillComeForm, self).__init__(*args, **kwargs)
    #     self.fields['will_come'].label = _('Will you participate in Tehran site competition?')
    #     self.fields['will_come'].widget.attrs = {
    #         'class': 'with-gap'
    #     }

    class Meta:
        model = Team
        fields = ('will_come',)
        widgets = {'will_come': forms.RadioSelect}


class GameTypeForm(forms.Form):
    game_type = forms.ChoiceField(choices=Game.GAME_TYPES, label=_('game type'), initial=2)
