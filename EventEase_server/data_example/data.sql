--
-- PostgreSQL database dump
--

-- Dumped from database version 15.2
-- Dumped by pg_dump version 15.2

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

--
-- Data for Name: accounts_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accounts_user (id, password, last_login, first_name, last_name, email, phone, is_service_provider, is_active, date_joined, is_superuser) FROM stdin;
1	pbkdf2_sha256$720000$uHzSYSJq9DNvhOci4qRkpS$tpkgfv95fjPKnN0LlU81vpkxIJ2BeVJTM0uTvf8Cz9Y=	2024-05-10 16:18:22.056513+03	mahdi	abo tafish	m1hdi1t@gmail.com	+963935925081	f	t	2024-05-10 14:55:55.817371+03	t
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: accounts_user_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accounts_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	contenttypes	contenttype
5	sessions	session
6	accounts	user
7	authtoken	token
8	authtoken	tokenproxy
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add session	5	add_session
18	Can change session	5	change_session
19	Can delete session	5	delete_session
20	Can view session	5	view_session
21	Can add user	6	add_user
22	Can change user	6	change_user
23	Can delete user	6	delete_user
24	Can view user	6	view_user
25	Can add Token	7	add_token
26	Can change Token	7	change_token
27	Can delete Token	7	delete_token
28	Can view Token	7	view_token
29	Can add Token	8	add_tokenproxy
30	Can change Token	8	change_tokenproxy
31	Can delete Token	8	delete_tokenproxy
32	Can view Token	8	view_tokenproxy
\.


--
-- Data for Name: accounts_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accounts_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: authtoken_token; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.authtoken_token (key, created, user_id) FROM stdin;
c26f6dbfd596daba9a304ec3100d6e793dea5ebc	2024-05-10 19:14:50.68862+03	1
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	accounts	0001_initial	2024-05-10 14:46:37.267006+03
2	contenttypes	0001_initial	2024-05-10 14:46:37.564752+03
3	admin	0001_initial	2024-05-10 14:46:38.602526+03
4	admin	0002_logentry_remove_auto_add	2024-05-10 14:46:38.668296+03
5	admin	0003_logentry_add_action_flag_choices	2024-05-10 14:46:38.799214+03
6	contenttypes	0002_remove_content_type_name	2024-05-10 14:46:38.893794+03
7	auth	0001_initial	2024-05-10 14:46:40.101452+03
8	auth	0002_alter_permission_name_max_length	2024-05-10 14:46:40.12648+03
9	auth	0003_alter_user_email_max_length	2024-05-10 14:46:40.135352+03
10	auth	0004_alter_user_username_opts	2024-05-10 14:46:40.148344+03
11	auth	0005_alter_user_last_login_null	2024-05-10 14:46:40.158334+03
12	auth	0006_require_contenttypes_0002	2024-05-10 14:46:40.161333+03
13	auth	0007_alter_validators_add_error_messages	2024-05-10 14:46:40.172328+03
14	auth	0008_alter_user_username_max_length	2024-05-10 14:46:40.180321+03
15	auth	0009_alter_user_last_name_max_length	2024-05-10 14:46:40.189316+03
16	auth	0010_alter_group_name_max_length	2024-05-10 14:46:40.218298+03
17	auth	0011_update_proxy_permissions	2024-05-10 14:46:40.227293+03
18	auth	0012_alter_user_first_name_max_length	2024-05-10 14:46:40.234288+03
19	sessions	0001_initial	2024-05-10 14:46:40.582432+03
20	accounts	0002_user_is_superuser	2024-05-10 14:51:41.258418+03
21	accounts	0003_user_groups_user_user_permissions	2024-05-10 16:32:54.143891+03
22	authtoken	0001_initial	2024-05-10 17:07:25.100037+03
23	authtoken	0002_auto_20160226_1747	2024-05-10 17:07:25.145176+03
24	authtoken	0003_tokenproxy	2024-05-10 17:07:25.149093+03
25	authtoken	0004_alter_tokenproxy_options	2024-05-10 17:07:25.157295+03
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
ns3fmqjxdxudzsdv6ovpwnjhk6po6f7l	.eJxVjMsOwiAUBf-FtSE8FKxL9_0GAtxzpWogKe3K-O_apAvdnpk5LxHiupSwdsxhInERWhx-txTzA3UDdI_11mRudZmnJDdF7rTLsRGe1939Oyixl29tvKXksiJwthYueWgfz8gGiZWxhk7QzqujBdhk9uABdmBtVCJ4Fu8PC5E5Iw:1s5Q8k:hR-Rtd9um6-KkPsHYXaOah6w-MMgR-X6tQWwyLQm4WI	2024-05-24 16:18:22.100785+03
\.


--
-- Name: accounts_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_user_groups_id_seq', 1, false);


--
-- Name: accounts_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_user_id_seq', 1, true);


--
-- Name: accounts_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_user_user_permissions_id_seq', 1, false);


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

SELECT pg_catalog.setval('public.auth_permission_id_seq', 32, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 8, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 25, true);


--
-- PostgreSQL database dump complete
--

