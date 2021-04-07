# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class ApiCdrOrigin(models.Model):
    seq = models.AutoField(primary_key=True)
    origin_body = models.TextField()
    origin_json = models.TextField()

    class Meta:
        managed = False
        db_table = 'api_cdr_origin'

class ApiCdrCall(models.Model):
    objects = models.Manager()
    session = models.CharField(primary_key=True, max_length=50)
    correlatorindex = models.IntegerField()
    record_type = models.CharField(max_length=100, blank=True, null=True)
    call_id = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    calltype = models.CharField(max_length=100, blank=True, null=True)
    cospace = models.CharField(max_length=100, blank=True, null=True)
    callcorrelator = models.CharField(max_length=100, blank=True, null=True)
    calllegscompleted = models.IntegerField(blank=True, null=True)
    calllegsmaxactive = models.IntegerField(blank=True, null=True)
    durationseconds = models.IntegerField(blank=True, null=True)
    cdrtag = models.CharField(max_length=100, blank=True, null=True)
    tenant = models.CharField(max_length=100, blank=True, null=True)
    source_ip = models.CharField(max_length=100, blank=True, null=True)
    add_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'api_cdr_call'
        unique_together = (('session', 'correlatorindex'),)


class ApiCdrCallleg(models.Model):
    seq = models.AutoField(primary_key=True)
    session = models.CharField(max_length=100)
    correlatorindex = models.IntegerField()
    record_type = models.CharField(max_length=100, blank=True, null=True)
    callleg_id = models.CharField(max_length=100, blank=True, null=True)
    cdrtag = models.CharField(max_length=100, blank=True, null=True)
    displayname = models.CharField(max_length=100, blank=True, null=True)
    guestconnection = models.CharField(max_length=100, blank=True, null=True)
    localaddress = models.CharField(max_length=100, blank=True, null=True)
    remoteaddress = models.CharField(max_length=100, blank=True, null=True)
    remoteparty = models.CharField(max_length=100, blank=True, null=True)
    recording = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    subtype = models.CharField(max_length=100, blank=True, null=True)
    lyncsubtype = models.CharField(max_length=100, blank=True, null=True)
    direction = models.CharField(max_length=100, blank=True, null=True)
    call = models.CharField(max_length=100, blank=True, null=True)
    ivr = models.CharField(max_length=100, blank=True, null=True)
    ownerid = models.CharField(max_length=100, blank=True, null=True)
    sipcallid = models.CharField(max_length=100, blank=True, null=True)
    replaces_sip_callid = models.CharField(max_length=100, blank=True, null=True)
    groupid = models.CharField(max_length=100, blank=True, null=True)
    reason = models.CharField(max_length=100, blank=True, null=True)
    remoteteardown = models.CharField(max_length=100, blank=True, null=True)
    durationseconds = models.IntegerField(blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    deactivated = models.CharField(max_length=100, blank=True, null=True)
    alarm_type = models.CharField(max_length=100, blank=True, null=True)
    alarm_durationpercentage = models.FloatField(blank=True, null=True)
    encryptedmedia = models.CharField(max_length=100, blank=True, null=True)
    unencryptedmedia = models.CharField(max_length=100, blank=True, null=True)
    canmove = models.CharField(max_length=5, blank=True, null=True)
    movedcallleg = models.CharField(max_length=100, blank=True, null=True)
    movedcalllegbridge = models.CharField(max_length=100, blank=True, null=True)
    mediausagepercentages_mainvideoviewer = models.FloatField(blank=True, null=True)
    mediausagepercentages_mainvideocontributor = models.FloatField(blank=True, null=True)
    mediausagepercentages_presentationviewer = models.FloatField(blank=True, null=True)
    mediausagepercentages_presentationcontributor = models.FloatField(blank=True, null=True)
    rxvideo_codec = models.CharField(max_length=100, blank=True, null=True)
    rxvideo_maxsizewidth = models.IntegerField(blank=True, null=True)
    rxvideo_maxsizeheight = models.IntegerField(blank=True, null=True)
    rxvideo_packetlossbursts_duration = models.FloatField(blank=True, null=True)
    rxvideo_packetlossbursts_density = models.FloatField(blank=True, null=True)
    rxvideo_packetgap_duration = models.FloatField(blank=True, null=True)
    rxvideo_packetgap_density = models.FloatField(blank=True, null=True)
    txvideo_codec = models.CharField(max_length=100, blank=True, null=True)
    txvideo_maxsizewidth = models.IntegerField(blank=True, null=True)
    txvideo_maxsizeheight = models.IntegerField(blank=True, null=True)
    txvideo_packetlossbursts_duration = models.FloatField(blank=True, null=True)
    txvideo_packetlossbursts_density = models.FloatField(blank=True, null=True)
    txvideo_packetgap_duration = models.FloatField(blank=True, null=True)
    txvideo_packetgap_density = models.FloatField(blank=True, null=True)
    rxaudio_codec = models.CharField(max_length=100, blank=True, null=True)
    rxaudio_packetlossbursts_duration = models.FloatField(blank=True, null=True)
    rxaudio_packetlossbursts_density = models.FloatField(blank=True, null=True)
    rxaudio_packetgap_duration = models.FloatField(blank=True, null=True)
    rxaudio_packetgap_density = models.FloatField(blank=True, null=True)
    txaudio_codec = models.CharField(max_length=100, blank=True, null=True)
    txaudio_packetlossbursts_duration = models.FloatField(blank=True, null=True)
    txaudio_packetlossbursts_density = models.FloatField(blank=True, null=True)
    txaudio_packetgap_duration = models.FloatField(blank=True, null=True)
    txaudio_packetgap_density = models.FloatField(blank=True, null=True)
    source_ip = models.CharField(max_length=100, blank=True, null=True)
    add_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    
    class Meta:
        managed = False
        db_table = 'api_cdr_callleg'
        unique_together = (('seq', 'session', 'correlatorindex'),)


class ApiCdrRecord(models.Model):
    session = models.CharField(primary_key=True, max_length=100)
    correlatorindex = models.IntegerField()
    type = models.CharField(max_length=100, blank=True, null=True)
    time = models.CharField(max_length=100, blank=True, null=True)
    recordindex = models.IntegerField(blank=True, null=True)
    add_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    utc_time = models.DateTimeField(blank=True, null=True)
    local_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'api_cdr_record'
        unique_together = (('session', 'correlatorindex'),)


class ApiCdrRecording(models.Model):
    session = models.CharField(primary_key=True, max_length=100)
    correlatorindex = models.IntegerField()
    record_type = models.CharField(max_length=100, blank=True, null=True)
    recording_id = models.CharField(max_length=100, blank=True, null=True)
    path = models.CharField(max_length=100, blank=True, null=True)
    recorderurl = models.CharField(max_length=100, blank=True, null=True)
    call = models.CharField(max_length=100, blank=True, null=True)
    callleg = models.CharField(max_length=100, blank=True, null=True)
    add_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'api_cdr_recording'
        unique_together = (('session', 'correlatorindex'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CeleryTaskmeta(models.Model):
    task_id = models.CharField(unique=True, max_length=255)
    status = models.CharField(max_length=50)
    result = models.TextField(blank=True, null=True)
    date_done = models.DateTimeField()
    traceback = models.TextField(blank=True, null=True)
    hidden = models.IntegerField()
    meta = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'celery_taskmeta'


class CeleryTasksetmeta(models.Model):
    taskset_id = models.CharField(unique=True, max_length=255)
    result = models.TextField()
    date_done = models.DateTimeField()
    hidden = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'celery_tasksetmeta'


class CmsCodeDetail(models.Model):
    seq = models.AutoField(primary_key=True)
    group_code = models.CharField(max_length=20)
    detail_code = models.CharField(max_length=20)
    code_name = models.CharField(max_length=100, blank=True, null=True)
    code_ename = models.CharField(max_length=100, blank=True, null=True)
    note = models.CharField(max_length=500, blank=True, null=True)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    order_no = models.IntegerField(blank=True, null=True)
    delete_yn = models.CharField(max_length=1, blank=True, null=True)
    regist_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    regist_id = models.CharField(max_length=50, blank=True, null=True)
    modify_date = models.DateTimeField(blank=True, null=True, auto_now=True)
    modify_id = models.CharField(max_length=50, blank=True, null=True)
    add_param1 = models.CharField(max_length=50, blank=True, null=True)
    add_param2 = models.CharField(max_length=100, blank=True, null=True)
    add_param3 = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cms_code_detail'


class CmsCodeGroup(models.Model):
    seq = models.AutoField(primary_key=True)
    group_code = models.CharField(max_length=20)
    group_name = models.CharField(max_length=100, blank=True, null=True)
    group_ename = models.CharField(max_length=100, blank=True, null=True)
    group_note = models.CharField(max_length=500, blank=True, null=True)
    delete_yn = models.CharField(max_length=1, blank=True, null=True)
    regist_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    regist_id = models.CharField(max_length=50, blank=True, null=True)
    modify_date = models.DateTimeField(blank=True, null=True, auto_now=True)
    modify_id = models.CharField(max_length=50, blank=True, null=True)
    add_param1 = models.CharField(max_length=50, blank=True, null=True)
    add_param2 = models.CharField(max_length=50, blank=True, null=True)
    add_param3 = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cms_code_group'


class CmsCospace(models.Model):
    cospace_seq = models.AutoField(primary_key=True)
    cospace_id = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    uri = models.CharField(max_length=100, blank=True, null=True)
    call_id = models.CharField(max_length=100, blank=True, null=True)
    passcode = models.CharField(max_length=100, blank=True, null=True)
    template_seq = models.CharField(max_length=100, blank=True, null=True)
    group_seq = models.IntegerField(blank=True, null=True)
    server_seq = models.IntegerField(blank=True, null=True)
    delete_yn = models.TextField(max_length=1, blank=True, null=True, default='N')
    regist_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    regist_id = models.CharField(max_length=100, blank=True, null=True)
    modify_date = models.DateTimeField(blank=True, null=True, auto_now=True)
    modify_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cms_cospace'


class CmsEndpoint(models.Model):
    ep_id = models.CharField(primary_key=True, max_length=100)
    ep_group_seq = models.CharField(max_length=100, blank=True, null=True)
    ep_name = models.CharField(max_length=100, blank=True, null=True)
    ep_type = models.CharField(max_length=100, blank=True, null=True)
    ip = models.CharField(max_length=100, blank=True, null=True)
    sip = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    recodingdevice = models.CharField(max_length=100, blank=True, null=True)
    audioonly = models.CharField(max_length=100, blank=True, null=True)
    hdevice = models.CharField(max_length=100, blank=True, null=True)
    mslync = models.CharField(max_length=100, blank=True, null=True)
    gmt_time = models.CharField(max_length=100, blank=True, null=True)
    ep_group_sub_seq = models.CharField(max_length=100, blank=True, null=True)
    order_no = models.IntegerField(blank=True, null=True)
    bandwidth = models.CharField(max_length=50, blank=True, null=True)
    delete_yn = models.CharField(max_length=100, blank=True, null=True)
    use_yn = models.CharField(max_length=1, blank=True, null=True)
    open_yn = models.CharField(max_length=1, blank=True, null=True)
    regist_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    regist_id = models.CharField(max_length=50, blank=True, null=True)
    modify_date = models.DateTimeField(blank=True, null=True)
    modify_id = models.CharField(max_length=50, blank=True, null=True)
    device_id = models.CharField(max_length=100, blank=True, null=True)
    device_pwd = models.CharField(max_length=500, blank=True, null=True)
    device_module = models.CharField(max_length=100, blank=True, null=True)
    device_open = models.CharField(max_length=100, blank=True, null=True)
    device_officer = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cms_endpoint'


class CmsEndpointGroup(models.Model):
    ep_group_seq = models.AutoField(primary_key=True)
    ep_group_name = models.CharField(max_length=100, blank=True, null=True)
    ep_group_color = models.CharField(max_length=100, blank=True, null=True)
    up_ep_group_seq = models.IntegerField(blank=True, null=True)
    order_no = models.IntegerField(blank=True, null=True)
    delete_yn = models.CharField(max_length=1, blank=True, null=True)
    regist_date = models.DateTimeField(auto_now_add=True)
    regist_id = models.CharField(max_length=50, blank=True, null=True)
    modify_date = models.DateTimeField(auto_now=True)
    modify_id = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cms_endpoint_group'


class CmsLdapserver(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    title = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    regist_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    regist_id = models.CharField(max_length=50, blank=True, null=True)
    modify_date = models.DateTimeField(blank=True, null=True, auto_now=True)
    modify_id = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cms_ldapserver'


class CmsLoginLog(models.Model):
    seq = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=8, blank=True, null=True)
    login_ip = models.CharField(max_length=20, blank=True, null=True)
    login_status = models.CharField(max_length=100, blank=True, null=True)
    login_date = models.DateTimeField(blank=True, null=True)
    logout_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cms_login_log'


class CmsManager(models.Model):
    user_id = models.CharField(primary_key=True, max_length=50)
    user_name = models.CharField(max_length=50)
    user_pwd = models.CharField(max_length=100)
    user_role = models.CharField(max_length=100)
    group_seq = models.CharField(max_length=100, blank=True, null=True)
    pw_change_date = models.DateTimeField(blank=True, null=True)
    login_fail_cnt = models.IntegerField(blank=True, null=True, default=0)
    last_login = models.DateTimeField(blank=True, null=True)
    language = models.CharField(max_length=20, blank=True, null=True, default='ko')
    delete_yn = models.CharField(max_length=1, blank=True, null=True, default='N')
    regist_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    regist_id = models.CharField(max_length=50, blank=True, null=True)
    modify_date = models.DateTimeField(blank=True, null=True, auto_now=True)
    modify_id = models.CharField(max_length=50, blank=True, null=True)
    expire_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cms_manager'


class CmsManagerGroup(models.Model):
    group_seq = models.CharField(primary_key=True, max_length=100)
    group_note = models.CharField(max_length=300)
    up_group_seq = models.CharField(max_length=100, blank=True, null=True)
    regist_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    modify_date = models.DateTimeField(blank=True, null=True, auto_now=True)
    delete_yn = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'cms_manager_group'


class CmsManagerMenu(models.Model):
    user_id = models.CharField(primary_key=True, max_length=50)
    menu_seq = models.IntegerField()
    regist_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    modify_date = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 'cms_manager_menu'
        unique_together = (('user_id', 'menu_seq'),)


class CmsMenu(models.Model):
    menu_seq = models.IntegerField()
    menu_name = models.CharField(max_length=100)
    up_menu_seq = models.IntegerField(blank=True, null=True)
    menu_url = models.CharField(max_length=500, blank=True, null=True)
    img_url = models.CharField(max_length=500, blank=True, null=True)
    sort_no = models.IntegerField(blank=True, null=True)
    regist_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    modify_date = models.DateTimeField(blank=True, null=True, auto_now=True)
    delete_yn = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'cms_menu'


class CmsMenuDefault(models.Model):
    menu_seq = models.IntegerField()
    user_role = models.CharField(max_length=500)
    default_yn = models.CharField(max_length=10, blank=True, null=True)
    regist_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    modify_date = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 'cms_menu_default'


class CmsTemplate(models.Model):
    seq = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    delete_yn = models.CharField(max_length=1, blank=True, null=True)
    callbrandingprofile = models.CharField(max_length=100, blank=True, null=True)
    calllegprofile = models.CharField(max_length=100, blank=True, null=True)
    callprofile = models.CharField(max_length=100, blank=True, null=True)
    dtmfprofile = models.CharField(max_length=100, blank=True, null=True)
    ivrbrandingprofile = models.CharField(max_length=100, blank=True, null=True)
    userprofile = models.CharField(max_length=100, blank=True, null=True)
    note = models.CharField(max_length=1000, blank=True, null=True)
    regist_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    regist_id = models.CharField(max_length=50, blank=True, null=True)
    modify_date = models.DateTimeField(blank=True, null=True, auto_now=True)
    modify_id = models.CharField(max_length=50, blank=True, null=True)
    group_seq = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cms_template'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DjceleryCrontabschedule(models.Model):
    minute = models.CharField(max_length=64)
    hour = models.CharField(max_length=64)
    day_of_week = models.CharField(max_length=64)
    day_of_month = models.CharField(max_length=64)
    month_of_year = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'djcelery_crontabschedule'


class DjceleryIntervalschedule(models.Model):
    every = models.IntegerField()
    period = models.CharField(max_length=24)

    class Meta:
        managed = False
        db_table = 'djcelery_intervalschedule'


class DjceleryPeriodictask(models.Model):
    name = models.CharField(unique=True, max_length=200)
    task = models.CharField(max_length=200)
    args = models.TextField()
    kwargs = models.TextField()
    queue = models.CharField(max_length=200, blank=True, null=True)
    exchange = models.CharField(max_length=200, blank=True, null=True)
    routing_key = models.CharField(max_length=200, blank=True, null=True)
    expires = models.DateTimeField(blank=True, null=True)
    enabled = models.IntegerField()
    last_run_at = models.DateTimeField(blank=True, null=True)
    total_run_count = models.PositiveIntegerField()
    date_changed = models.DateTimeField()
    description = models.TextField()
    crontab = models.ForeignKey(DjceleryCrontabschedule, models.DO_NOTHING, blank=True, null=True)
    interval = models.ForeignKey(DjceleryIntervalschedule, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djcelery_periodictask'


class DjceleryPeriodictasks(models.Model):
    ident = models.SmallIntegerField(primary_key=True)
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'djcelery_periodictasks'


class DjceleryTaskstate(models.Model):
    state = models.CharField(max_length=64)
    task_id = models.CharField(unique=True, max_length=36)
    name = models.CharField(max_length=200, blank=True, null=True)
    tstamp = models.DateTimeField()
    args = models.TextField(blank=True, null=True)
    kwargs = models.TextField(blank=True, null=True)
    eta = models.DateTimeField(blank=True, null=True)
    expires = models.DateTimeField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)
    traceback = models.TextField(blank=True, null=True)
    runtime = models.FloatField(blank=True, null=True)
    retries = models.IntegerField()
    hidden = models.IntegerField()
    worker = models.ForeignKey('DjceleryWorkerstate', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djcelery_taskstate'


class DjceleryWorkerstate(models.Model):
    hostname = models.CharField(unique=True, max_length=255)
    last_heartbeat = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djcelery_workerstate'

class CmsLayoutTemplate(models.Model):
    inter_id = models.IntegerField(blank=True, null=True)
    template_id = models.CharField(max_length=100, blank=True, null=True)
    template_name = models.CharField(max_length=50, blank=True, null=True)
    tm_json = models.TextField(blank=True, null=True)
    cisco_json = models.TextField(blank=True, null=True)
    del_yn = models.CharField(max_length=5, default='N')
    fst_regr_id = models.CharField(max_length=50, blank=True, null=True)
    # fst_reg_dt = models.DateTimeField(blank=True, null=True)
    fnl_mdfr_id = models.CharField(max_length=50, blank=True, null=True)
    # fnl_mdfy_dt = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cms_layout_template'