--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4
-- Dumped by pg_dump version 16.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: chat_groupis; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.chat_groupis (
    id bigint NOT NULL,
    name character varying(200) NOT NULL,
    description text,
    updated timestamp with time zone NOT NULL,
    created timestamp with time zone NOT NULL,
    host_id bigint
);


ALTER TABLE public.chat_groupis OWNER TO postgres;

--
-- Name: chat_groupis_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.chat_groupis ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.chat_groupis_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: chat_groupis_participants; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.chat_groupis_participants (
    id bigint NOT NULL,
    groupis_id bigint NOT NULL,
    myuser_id bigint NOT NULL
);


ALTER TABLE public.chat_groupis_participants OWNER TO postgres;

--
-- Name: chat_groupis_participants_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.chat_groupis_participants ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.chat_groupis_participants_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: chat_message; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.chat_message (
    id bigint NOT NULL,
    body text NOT NULL,
    updated timestamp with time zone NOT NULL,
    created timestamp with time zone NOT NULL,
    group_id bigint NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.chat_message OWNER TO postgres;

--
-- Name: chat_message_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.chat_message ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.chat_message_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: chat_myuser; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.chat_myuser (
    id bigint NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.chat_myuser OWNER TO postgres;

--
-- Name: chat_myuser_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.chat_myuser_groups (
    id bigint NOT NULL,
    myuser_id bigint NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.chat_myuser_groups OWNER TO postgres;

--
-- Name: chat_myuser_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.chat_myuser_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.chat_myuser_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: chat_myuser_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.chat_myuser ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.chat_myuser_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: chat_myuser_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.chat_myuser_user_permissions (
    id bigint NOT NULL,
    myuser_id bigint NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.chat_myuser_user_permissions OWNER TO postgres;

--
-- Name: chat_myuser_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.chat_myuser_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.chat_myuser_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: chat_otpdevice; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.chat_otpdevice (
    id bigint NOT NULL,
    name character varying(64) NOT NULL,
    confirmed boolean NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.chat_otpdevice OWNER TO postgres;

--
-- Name: chat_otpdevice_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.chat_otpdevice ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.chat_otpdevice_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id bigint NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- Name: otp_totp_totpdevice; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.otp_totp_totpdevice (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    confirmed boolean NOT NULL,
    throttling_failure_timestamp timestamp with time zone,
    throttling_failure_count integer NOT NULL,
    created_at timestamp with time zone,
    last_used_at timestamp with time zone,
    key character varying(80) NOT NULL,
    step smallint NOT NULL,
    t0 bigint NOT NULL,
    digits smallint NOT NULL,
    tolerance smallint NOT NULL,
    drift smallint NOT NULL,
    last_t bigint NOT NULL,
    user_id bigint NOT NULL,
    CONSTRAINT otp_totp_totpdevice_digits_check CHECK ((digits >= 0)),
    CONSTRAINT otp_totp_totpdevice_step_check CHECK ((step >= 0)),
    CONSTRAINT otp_totp_totpdevice_throttling_failure_count_check CHECK ((throttling_failure_count >= 0)),
    CONSTRAINT otp_totp_totpdevice_tolerance_check CHECK ((tolerance >= 0))
);


ALTER TABLE public.otp_totp_totpdevice OWNER TO postgres;

--
-- Name: otp_totp_totpdevice_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.otp_totp_totpdevice ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.otp_totp_totpdevice_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add permission	1	add_permission
2	Can change permission	1	change_permission
3	Can delete permission	1	delete_permission
4	Can view permission	1	view_permission
5	Can add group	2	add_group
6	Can change group	2	change_group
7	Can delete group	2	delete_group
8	Can view group	2	view_group
9	Can add content type	3	add_contenttype
10	Can change content type	3	change_contenttype
11	Can delete content type	3	delete_contenttype
12	Can view content type	3	view_contenttype
13	Can add session	4	add_session
14	Can change session	4	change_session
15	Can delete session	4	delete_session
16	Can view session	4	view_session
17	Can add log entry	5	add_logentry
18	Can change log entry	5	change_logentry
19	Can delete log entry	5	delete_logentry
20	Can view log entry	5	view_logentry
21	Can add TOTP device	6	add_totpdevice
22	Can change TOTP device	6	change_totpdevice
23	Can delete TOTP device	6	delete_totpdevice
24	Can view TOTP device	6	view_totpdevice
25	Can add user	7	add_myuser
26	Can change user	7	change_myuser
27	Can delete user	7	delete_myuser
28	Can view user	7	view_myuser
29	Can add group is	8	add_groupis
30	Can change group is	8	change_groupis
31	Can delete group is	8	delete_groupis
32	Can view group is	8	view_groupis
33	Can add message	9	add_message
34	Can change message	9	change_message
35	Can delete message	9	delete_message
36	Can view message	9	view_message
37	Can add otp device	10	add_otpdevice
38	Can change otp device	10	change_otpdevice
39	Can delete otp device	10	delete_otpdevice
40	Can view otp device	10	view_otpdevice
41	Can add user status	11	add_userstatus
42	Can change user status	11	change_userstatus
43	Can delete user status	11	delete_userstatus
44	Can view user status	11	view_userstatus
\.


--
-- Data for Name: chat_groupis; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.chat_groupis (id, name, description, updated, created, host_id) FROM stdin;
11	Banda	My name is Bekrahoon and I am the main person in this group! I want you to be kind and active.	2024-09-01 01:02:03.36349+05	2024-09-01 01:02:03.36349+05	1
13	100 pull ups challenge	Who can do this!?	2024-09-01 01:24:35.597443+05	2024-09-01 01:24:35.597443+05	3
14	laptops		2024-09-01 17:08:42.924206+05	2024-09-01 17:04:42.155038+05	3
\.


--
-- Data for Name: chat_groupis_participants; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.chat_groupis_participants (id, groupis_id, myuser_id) FROM stdin;
98	11	1
99	11	4
100	13	3
101	11	3
102	14	1
103	14	2
104	14	3
105	14	4
106	14	5
107	14	6
\.


--
-- Data for Name: chat_message; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.chat_message (id, body, updated, created, group_id, user_id) FROM stdin;
101	Hello everyone!	2024-09-01 01:02:19.292168+05	2024-09-01 01:02:19.292168+05	11	1
102	hello Bekrahoon	2024-09-01 01:20:31.989071+05	2024-09-01 01:20:31.989071+05	11	4
103	hello	2024-09-01 01:57:20.781606+05	2024-09-01 01:57:20.781606+05	13	3
104	hi	2024-09-01 17:03:57.223808+05	2024-09-01 17:03:57.224317+05	11	3
\.


--
-- Data for Name: chat_myuser; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.chat_myuser (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
5	pbkdf2_sha256$600000$kGQXtvrtYfc70rIaI87qnU$QhTDeQXpkUCMHApCEJQ0ioaaPbUmlR8fU4yONreVCVo=	2024-09-01 00:49:25.917427+05	f	Geradot			Dzastinbuber@email.com	f	t	2024-08-31 00:44:47.662161+05
2	pbkdf2_sha256$600000$MawcbQ1Ijou10tFnMcjACV$Q+O7OXzLUB6QEGpdK5pP2G2UNTxVeQF3CHRw9X27oRg=	2024-09-01 00:57:59.389362+05	f	Muhammed			muhammed@email.com	f	t	2024-08-29 21:58:23.132725+05
1	pbkdf2_sha256$600000$QGBaqTcBhGofijBqppITaJ$YoJ/AZIj4v4U91wHd/UVM1lXjS43WP3vDAuKg/5lkWQ=	2024-09-01 01:22:59.13596+05	t	Bekrahoon			bekrahoo@email.com	t	t	2024-08-29 21:46:59.159411+05
3	pbkdf2_sha256$600000$05v1SruXVomb5vyFTXZTwP$xbD7Sq9GnGTi7+A6gQt6OJB7F8mLSWwVtU7zlc2zaOU=	2024-09-01 17:03:43.747113+05	f	Ben			amir862@gmail.com	f	t	2024-08-29 22:21:09.844432+05
4	pbkdf2_sha256$600000$r225pESHzo8btjWqj1SRSJ$GxNqITOV59urUE17rtDrm/zEFWEcAFy90IKHVW2jvkw=	2024-09-01 17:09:41.064002+05	f	Amir			amir862@gmail.com	f	t	2024-08-30 02:28:00.822467+05
6	pbkdf2_sha256$600000$i5BRjgsrc2Cq4D1MFU6aWD$aSW9NVypqlsGd3I5nPgH+SpsgjdzFnjVNSafC8SjxSw=	2024-09-01 00:46:54.479539+05	f	Fernando			fernando@gmail.com	f	t	2024-09-01 00:46:53.396756+05
\.


--
-- Data for Name: chat_myuser_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.chat_myuser_groups (id, myuser_id, group_id) FROM stdin;
\.


--
-- Data for Name: chat_myuser_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.chat_myuser_user_permissions (id, myuser_id, permission_id) FROM stdin;
\.


--
-- Data for Name: chat_otpdevice; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.chat_otpdevice (id, name, confirmed, user_id) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2024-08-30 14:27:02.208375+05	19	Bekrahoon:hello guis!	1	[{"added": {}}]	9	1
2	2024-08-30 14:29:01.69516+05	20	Bekrahoon:Hi	1	[{"added": {}}]	9	1
3	2024-08-30 14:29:15.503212+05	21	Ben:hello	1	[{"added": {}}]	9	1
4	2024-09-01 00:28:22.326147+05	1	Example Group	2	[{"changed": {"fields": ["Host", "Participants"]}}]	8	1
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	auth	permission
2	auth	group
3	contenttypes	contenttype
4	sessions	session
5	admin	logentry
6	otp_totp	totpdevice
7	chat	myuser
8	chat	groupis
9	chat	message
10	chat	otpdevice
11	chat	userstatus
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2024-08-29 21:44:45.602074+05
2	contenttypes	0002_remove_content_type_name	2024-08-29 21:44:45.610763+05
3	auth	0001_initial	2024-08-29 21:44:45.674006+05
4	auth	0002_alter_permission_name_max_length	2024-08-29 21:44:45.67904+05
5	auth	0003_alter_user_email_max_length	2024-08-29 21:44:45.685083+05
6	auth	0004_alter_user_username_opts	2024-08-29 21:44:45.692687+05
7	auth	0005_alter_user_last_login_null	2024-08-29 21:44:45.699246+05
8	auth	0006_require_contenttypes_0002	2024-08-29 21:44:45.702234+05
9	auth	0007_alter_validators_add_error_messages	2024-08-29 21:44:45.708768+05
10	auth	0008_alter_user_username_max_length	2024-08-29 21:44:45.713798+05
11	auth	0009_alter_user_last_name_max_length	2024-08-29 21:44:45.721825+05
12	auth	0010_alter_group_name_max_length	2024-08-29 21:44:45.731187+05
13	auth	0011_update_proxy_permissions	2024-08-29 21:44:45.73841+05
14	auth	0012_alter_user_first_name_max_length	2024-08-29 21:44:45.742432+05
15	chat	0001_initial	2024-08-29 21:44:45.870656+05
16	admin	0001_initial	2024-08-29 21:44:45.907585+05
17	admin	0002_logentry_remove_auto_add	2024-08-29 21:44:45.919129+05
18	admin	0003_logentry_add_action_flag_choices	2024-08-29 21:44:45.932638+05
19	otp_totp	0001_initial	2024-08-29 21:44:45.962363+05
20	sessions	0001_initial	2024-08-29 21:44:45.982273+05
21	chat	0002_alter_groupis_options_alter_message_options	2024-08-30 14:07:34.002964+05
22	chat	0003_alter_groupis_name_alter_message_group	2024-08-30 20:36:00.183463+05
23	chat	0004_alter_message_group	2024-08-31 12:59:52.062322+05
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
8271skn28jg4m16mj2atzyw4w1gal4xx	.eJxVjDEOwjAMRe-SGUUQ13FhZO8ZKttxaAGlUtNOiLtDpQ6w_vfef7me12Xo12pzPyZ3cY07_G7C-rCygXTncpu8TmWZR_Gb4ndafTcle1539-9g4Dp8a42KRhCPJ1AhBBJiEmgjB4sWs2YEROJzwoaNswqE1kgDUGoNo3t_AOurOEc:1skjOn:n5Uhee1nKoeQRwUqK31Upgw1tyJDhpZqLJCVLLIgDF8	2024-09-15 17:09:41.070676+05
5l4zghysdvqzdut29vuruc3yzp4v3o08	.eJxVjDEOwjAMRe-SGUV24iYRIztnqGI7JQXUSk07Ie4OlTrA-t97_2X6vK2131pZ-lHN2Xhz-t04y6NMO9B7nm6zlXlal5HtrtiDNnudtTwvh_t3UHOr35pD7nhI0lGH4DXGACjRO4gOgQGd-ESqTEIYAqYkigNkYibiWMC8P8FCNxs:1sk8ce:qjCGouit9tfk_vgRmL4zfSha8w9k9Vzuf-Zg7Njhq6A	2024-09-14 01:53:32.515394+05
\.


--
-- Data for Name: otp_totp_totpdevice; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.otp_totp_totpdevice (id, name, confirmed, throttling_failure_timestamp, throttling_failure_count, created_at, last_used_at, key, step, t0, digits, tolerance, drift, last_t, user_id) FROM stdin;
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 44, true);


--
-- Name: chat_groupis_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.chat_groupis_id_seq', 14, true);


--
-- Name: chat_groupis_participants_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.chat_groupis_participants_id_seq', 107, true);


--
-- Name: chat_message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.chat_message_id_seq', 104, true);


--
-- Name: chat_myuser_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.chat_myuser_groups_id_seq', 1, false);


--
-- Name: chat_myuser_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.chat_myuser_id_seq', 6, true);


--
-- Name: chat_myuser_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.chat_myuser_user_permissions_id_seq', 1, false);


--
-- Name: chat_otpdevice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.chat_otpdevice_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 4, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 11, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 23, true);


--
-- Name: otp_totp_totpdevice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.otp_totp_totpdevice_id_seq', 1, false);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: chat_groupis chat_groupis_name_0618bf9c_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_groupis
    ADD CONSTRAINT chat_groupis_name_0618bf9c_uniq UNIQUE (name);


--
-- Name: chat_groupis_participants chat_groupis_participants_groupis_id_myuser_id_59a30888_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_groupis_participants
    ADD CONSTRAINT chat_groupis_participants_groupis_id_myuser_id_59a30888_uniq UNIQUE (groupis_id, myuser_id);


--
-- Name: chat_groupis_participants chat_groupis_participants_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_groupis_participants
    ADD CONSTRAINT chat_groupis_participants_pkey PRIMARY KEY (id);


--
-- Name: chat_groupis chat_groupis_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_groupis
    ADD CONSTRAINT chat_groupis_pkey PRIMARY KEY (id);


--
-- Name: chat_message chat_message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_message
    ADD CONSTRAINT chat_message_pkey PRIMARY KEY (id);


--
-- Name: chat_myuser_groups chat_myuser_groups_myuser_id_group_id_addfe7df_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_myuser_groups
    ADD CONSTRAINT chat_myuser_groups_myuser_id_group_id_addfe7df_uniq UNIQUE (myuser_id, group_id);


--
-- Name: chat_myuser_groups chat_myuser_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_myuser_groups
    ADD CONSTRAINT chat_myuser_groups_pkey PRIMARY KEY (id);


--
-- Name: chat_myuser chat_myuser_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_myuser
    ADD CONSTRAINT chat_myuser_pkey PRIMARY KEY (id);


--
-- Name: chat_myuser_user_permissions chat_myuser_user_permiss_myuser_id_permission_id_0712f9c5_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_myuser_user_permissions
    ADD CONSTRAINT chat_myuser_user_permiss_myuser_id_permission_id_0712f9c5_uniq UNIQUE (myuser_id, permission_id);


--
-- Name: chat_myuser_user_permissions chat_myuser_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_myuser_user_permissions
    ADD CONSTRAINT chat_myuser_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: chat_myuser chat_myuser_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_myuser
    ADD CONSTRAINT chat_myuser_username_key UNIQUE (username);


--
-- Name: chat_otpdevice chat_otpdevice_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_otpdevice
    ADD CONSTRAINT chat_otpdevice_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: otp_totp_totpdevice otp_totp_totpdevice_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.otp_totp_totpdevice
    ADD CONSTRAINT otp_totp_totpdevice_pkey PRIMARY KEY (id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: chat_groupis_host_id_cacd2645; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX chat_groupis_host_id_cacd2645 ON public.chat_groupis USING btree (host_id);


--
-- Name: chat_groupis_name_0618bf9c_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX chat_groupis_name_0618bf9c_like ON public.chat_groupis USING btree (name varchar_pattern_ops);


--
-- Name: chat_groupis_participants_groupis_id_f4d22200; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX chat_groupis_participants_groupis_id_f4d22200 ON public.chat_groupis_participants USING btree (groupis_id);


--
-- Name: chat_groupis_participants_myuser_id_026837a1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX chat_groupis_participants_myuser_id_026837a1 ON public.chat_groupis_participants USING btree (myuser_id);


--
-- Name: chat_message_group_id_1d135dcf; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX chat_message_group_id_1d135dcf ON public.chat_message USING btree (group_id);


--
-- Name: chat_message_user_id_a47c01bb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX chat_message_user_id_a47c01bb ON public.chat_message USING btree (user_id);


--
-- Name: chat_myuser_groups_group_id_eb18d224; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX chat_myuser_groups_group_id_eb18d224 ON public.chat_myuser_groups USING btree (group_id);


--
-- Name: chat_myuser_groups_myuser_id_962ea6c1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX chat_myuser_groups_myuser_id_962ea6c1 ON public.chat_myuser_groups USING btree (myuser_id);


--
-- Name: chat_myuser_user_permissions_myuser_id_5d0a3bc6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX chat_myuser_user_permissions_myuser_id_5d0a3bc6 ON public.chat_myuser_user_permissions USING btree (myuser_id);


--
-- Name: chat_myuser_user_permissions_permission_id_665f9742; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX chat_myuser_user_permissions_permission_id_665f9742 ON public.chat_myuser_user_permissions USING btree (permission_id);


--
-- Name: chat_myuser_username_c7bf4a37_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX chat_myuser_username_c7bf4a37_like ON public.chat_myuser USING btree (username varchar_pattern_ops);


--
-- Name: chat_otpdevice_user_id_3f17d000; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX chat_otpdevice_user_id_3f17d000 ON public.chat_otpdevice USING btree (user_id);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: otp_totp_totpdevice_user_id_0fb18292; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX otp_totp_totpdevice_user_id_0fb18292 ON public.otp_totp_totpdevice USING btree (user_id);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: chat_groupis chat_groupis_host_id_cacd2645_fk_chat_myuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_groupis
    ADD CONSTRAINT chat_groupis_host_id_cacd2645_fk_chat_myuser_id FOREIGN KEY (host_id) REFERENCES public.chat_myuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: chat_groupis_participants chat_groupis_partici_groupis_id_f4d22200_fk_chat_grou; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_groupis_participants
    ADD CONSTRAINT chat_groupis_partici_groupis_id_f4d22200_fk_chat_grou FOREIGN KEY (groupis_id) REFERENCES public.chat_groupis(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: chat_groupis_participants chat_groupis_participants_myuser_id_026837a1_fk_chat_myuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_groupis_participants
    ADD CONSTRAINT chat_groupis_participants_myuser_id_026837a1_fk_chat_myuser_id FOREIGN KEY (myuser_id) REFERENCES public.chat_myuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: chat_message chat_message_group_id_1d135dcf_fk_chat_groupis_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_message
    ADD CONSTRAINT chat_message_group_id_1d135dcf_fk_chat_groupis_id FOREIGN KEY (group_id) REFERENCES public.chat_groupis(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: chat_message chat_message_user_id_a47c01bb_fk_chat_myuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_message
    ADD CONSTRAINT chat_message_user_id_a47c01bb_fk_chat_myuser_id FOREIGN KEY (user_id) REFERENCES public.chat_myuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: chat_myuser_groups chat_myuser_groups_group_id_eb18d224_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_myuser_groups
    ADD CONSTRAINT chat_myuser_groups_group_id_eb18d224_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: chat_myuser_groups chat_myuser_groups_myuser_id_962ea6c1_fk_chat_myuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_myuser_groups
    ADD CONSTRAINT chat_myuser_groups_myuser_id_962ea6c1_fk_chat_myuser_id FOREIGN KEY (myuser_id) REFERENCES public.chat_myuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: chat_myuser_user_permissions chat_myuser_user_per_myuser_id_5d0a3bc6_fk_chat_myus; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_myuser_user_permissions
    ADD CONSTRAINT chat_myuser_user_per_myuser_id_5d0a3bc6_fk_chat_myus FOREIGN KEY (myuser_id) REFERENCES public.chat_myuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: chat_myuser_user_permissions chat_myuser_user_per_permission_id_665f9742_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_myuser_user_permissions
    ADD CONSTRAINT chat_myuser_user_per_permission_id_665f9742_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: chat_otpdevice chat_otpdevice_user_id_3f17d000_fk_chat_myuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_otpdevice
    ADD CONSTRAINT chat_otpdevice_user_id_3f17d000_fk_chat_myuser_id FOREIGN KEY (user_id) REFERENCES public.chat_myuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_chat_myuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_chat_myuser_id FOREIGN KEY (user_id) REFERENCES public.chat_myuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: otp_totp_totpdevice otp_totp_totpdevice_user_id_0fb18292_fk_chat_myuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.otp_totp_totpdevice
    ADD CONSTRAINT otp_totp_totpdevice_user_id_0fb18292_fk_chat_myuser_id FOREIGN KEY (user_id) REFERENCES public.chat_myuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

