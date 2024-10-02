from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from views.chat import (
    ChatFileUploadApi,
    GroupDeleteView,
    deleteMessage,
    group,
    home,
    get_or_create_chat,
    GroupCreateView,
    UpdateMessageStatusApi,
    GroupUpdateView,
)
from views.notis import SaveFcmTokenView, showFirebaseJS
from views.otp import resend_otp, VerifyOTPView
from views.users import (
    change_login,
    LoginPageView,
    logoutUser,
    participants,
    RegisterPageView,
    UserProfileView,
    ProfileUpdateView,
    suspended_view,
)


urlpatterns = [
    path("accounts/login/", LoginPageView.as_view(), name="login"),
    path("logout/", logoutUser, name="logout"),
    path("register/", RegisterPageView.as_view(), name="register"),
    path("verify_otp/", VerifyOTPView.as_view(), name="verify_otp"),
    path("resend_otp/", resend_otp, name="resend_otp"),
    path("profile/<int:pk>/", UserProfileView.as_view(), name="user_profile"),
    path("change-login/", change_login, name="change_login"),
    path("", home, name="home"),
    path("group/<str:pk>/", group, name="group"),
    path("profile/<str:pk>/", UserProfileView.as_view(), name="user-profile"),
    path("participants/<str:pk>/", participants, name="participants"),
    path("profile/update/<int:pk>/", ProfileUpdateView.as_view(), name="update_profile"),
    path("suspended/", suspended_view, name="suspended"),
    path("chat/<int:pk>/", get_or_create_chat, name="start-chat"),
    path("chat/room/<int:pk>/", group, name="chatrooms"),
    path("create-group/", GroupCreateView.as_view(), name="create-group"),
    path("update-group/<str:pk>/", GroupUpdateView.as_view(), name="update-group"),
    path("delete-group/<str:pk>/", GroupDeleteView.as_view(), name="delete-group"),
    path("delete-message/<str:pk>/", deleteMessage, name="delete-message"),
    path(
        "update-message-status/<int:message_id>/",
        UpdateMessageStatusApi.as_view(),
        name="update_message_status",
    ),
    path("group/<int:pk>/file/upload/", ChatFileUploadApi.as_view(), name="chat_file_upload"),
    path("firebase-messaging-sw.js", showFirebaseJS, name="show_firebase_js"),
    path(
        "save-fcm-token/", SaveFcmTokenView.as_view(), name="save_fcm_token"
    ),  # Маршрут для сохранения FCM токена
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
