from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from views.chat import (
    chat_file_upload,
    deleteGroup,
    deleteMessage,
    group,
    home,
    get_or_create_chat,
    createGroup,
    update_message_status,
    updateGroup,
)
from views.notis import save_fcm_token, showFirebaseJS
from views.otp import resend_otp, verify_otp
from views.users import (
    change_login,
    loginPage,
    logoutUser,
    participants,
    registerPage,
    userProfile,
    profile_update,
    suspended_view,
)


urlpatterns = [
    path("accounts/login/", loginPage, name="login"),
    path("logout/", logoutUser, name="logout"),
    path("register/", registerPage, name="register"),
    path("verify_otp/", verify_otp, name="verify_otp"),
    path("resend_otp/", resend_otp, name="resend_otp"),
    path("profile/<int:pk>/", userProfile, name="user_profile"),
    path("change-login/", change_login, name="change_login"),
    path("", home, name="home"),
    path("group/<str:pk>/", group, name="group"),
    path("profile/<str:pk>/", userProfile, name="user-profile"),
    path("participants/<str:pk>/", participants, name="participants"),
    path("profile/update/<int:pk>/", profile_update, name="update_profile"),
    path("suspended/", suspended_view, name="suspended"),
    path("chat/<int:pk>/", get_or_create_chat, name="start-chat"),
    path("chat/room/<int:pk>/", group, name="chatrooms"),
    path("create-group/", createGroup, name="create-group"),
    path("update-group/<str:pk>/", updateGroup, name="update-group"),
    path("delete-group/<str:pk>/", deleteGroup, name="delete-group"),
    path("delete-message/<str:pk>/", deleteMessage, name="delete-message"),
    path(
        "update-message-status/<int:message_id>/",
        update_message_status,
        name="update_message_status",
    ),
    path("group/<int:pk>/file/upload/", chat_file_upload, name="chat_file_upload"),
    path("firebase-messaging-sw.js", showFirebaseJS, name="show_firebase_js"),
    path(
        "save-fcm-token/", save_fcm_token, name="save_fcm_token"
    ),  # Маршрут для сохранения FCM токена
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
