from django.contrib import messages

from core.utils import set_registry
from proposals.models import TalkProposal, TutorialProposal


@set_registry(**{'proposals.creatable': False})
def test_talk_proposal_create_unavailable(user_client):
    response = user_client.get('/en-us/proposals/talk/submit/')
    assert response.status_code == 404


@set_registry(**{'proposals.creatable': False})
def test_tutorial_proposal_create_unavailable(user_client):
    response = user_client.get('/en-us/proposals/tutorial/submit/')
    assert response.status_code == 404


@set_registry(**{'proposals.creatable': True})
def test_talk_proposal_create_login(db, client):
    response = client.get('/en-us/proposals/talk/submit/', follow=True)
    assert response.redirect_chain == [
        ('/en-us/accounts/login/?next=/en-us/proposals/talk/submit/', 302),
    ]


@set_registry(**{'proposals.creatable': True})
def test_tutorial_proposal_create_login(db, client):
    response = client.get('/en-us/proposals/tutorial/submit/', follow=True)
    assert response.redirect_chain == [
        ('/en-us/accounts/login/?next=/en-us/proposals/tutorial/submit/', 302),
    ]


@set_registry(**{'proposals.creatable': True})
def test_talk_proposal_create_denied_get(bare_user_client):
    response = bare_user_client.get('/en-us/proposals/talk/submit/')
    assert response.status_code == 403


@set_registry(**{'proposals.creatable': True})
def test_tutorial_proposal_create_denied_get(bare_user_client):
    response = bare_user_client.get('/en-us/proposals/tutorial/submit/')
    assert response.status_code == 403


@set_registry(**{'proposals.creatable': True})
def test_talk_proposal_create_denied_post(bare_user_client):
    response = bare_user_client.post('/en-us/proposals/talk/submit/')
    assert response.status_code == 403


@set_registry(**{'proposals.creatable': True})
def test_tutorial_proposal_create_denied_post(bare_user_client):
    response = bare_user_client.post('/en-us/proposals/tutorial/submit/')
    assert response.status_code == 403


@set_registry(**{'proposals.creatable': True})
def test_talk_proposal_create_get_coc(user, user_client):
    response = user_client.get('/en-us/proposals/talk/submit/', follow=True)
    assert response.redirect_chain == [
        ('/en-us/accounts/agreement/?next=/en-us/proposals/talk/submit/', 302),
    ]


@set_registry(**{'proposals.creatable': True})
def test_tutorial_proposal_create_get_coc(user, user_client):
    response = user_client.get('/en-us/proposals/tutorial/submit/', follow=True)
    assert response.redirect_chain == [
        ('/en-us/accounts/agreement/?next=/en-us/proposals/tutorial/submit/', 302),
    ]


@set_registry(**{'proposals.creatable': True})
def test_talk_proposal_create_get(agreed_user_client):
    response = agreed_user_client.get('/en-us/proposals/talk/submit/')
    assert response.status_code == 200


@set_registry(**{'proposals.creatable': True})
def test_tutorial_proposal_create_get(agreed_user_client):
    response = agreed_user_client.get('/en-us/proposals/tutorial/submit/')
    assert response.status_code == 200


@set_registry(**{'proposals.creatable': True})
def test_talk_proposal_create_post(agreed_user, agreed_user_client):
    response = agreed_user_client.post('/en-us/proposals/talk/submit/', {
        'title': 'Beyond the Style Guides<br>',
        'category': 'PRAC',
        'duration': 'PREF15',
        'language': 'ENEN',
        'python_level': 'INTERMEDIATE',
        'recording_policy': True,
        'live_stream_policy': True,
        'referring_policy': False,
        'first_time_speaker': True,
        'living_in_taiwan': True,
        'attend_in_person': True,
    }, follow=True)

    proposal = TalkProposal.objects.get(
        submitter=agreed_user,
        title='Beyond the Style Guides<br>',
    )
    assert response.redirect_chain == [
        (f'/en-us/proposals/talk/{proposal.pk}/edit/', 302),
    ], response.context['form'].errors

    msgs = [(m.level, m.message) for m in response.context['messages']]
    assert msgs == [
        (messages.SUCCESS,
         'Talk proposal '
         '<strong>Beyond the Style Guides&lt;br&gt;</strong> created.'),
    ]


@set_registry(**{'proposals.creatable': True})
def test_tutorial_proposal_create_post(agreed_user, agreed_user_client):
    response = agreed_user_client.post('/en-us/proposals/tutorial/submit/', {
        'title': 'Beyond the Style Guides<br>',
        'category': 'PRAC',
        'duration': 'FULLDAY',
        'language': 'ENEN',
        'python_level': 'INTERMEDIATE',
        'recording_policy': True,
        'live_stream_policy': True,
        'living_in_taiwan': True,
        'attend_in_person': True,
    }, follow=True)

    proposal = TutorialProposal.objects.get(
        submitter=agreed_user,
        title='Beyond the Style Guides<br>',
    )
    assert response.redirect_chain == [
        (f'/en-us/proposals/tutorial/{proposal.pk}/edit/', 302),
    ], response.context['form'].errors

    msgs = [(m.level, m.message) for m in response.context['messages']]
    assert msgs == [
        (messages.SUCCESS,
         'Tutorial proposal '
         '<strong>Beyond the Style Guides&lt;br&gt;</strong> created.'),
    ]
