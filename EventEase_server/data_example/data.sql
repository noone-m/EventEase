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
1	pbkdf2_sha256$720000$Ns0yUdTRpJq1WqrJqvi0Ro$VwUkWcwvEjHI7nfGygLVROpGaXixK1obIFmwLRi/FdU=	\N	mahdi	abo tafish	mahdi@gmail.com	+963935925081	f	t	2024-07-15 16:00:57.647029+03	t
2	pbkdf2_sha256$720000$llGSrTVbGwvuApSfnKUl1G$ZHBZZLkcTRVrBknKY0JVhA6zA+YdwkBWdug2Z5vAtZc=	\N	mahdi	at	m1hdi1t@gmail.com	+963935925081	t	t	2024-07-15 16:01:08.837948+03	f
3	pbkdf2_sha256$720000$GJ8cCWWEhnffAT2tGKmHMW$kLPJlRc6/kHOOSMQhbyU9SfdWt1gLsXpjerB0OTVRSU=	\N	danial	daibs	danial@gmail.com	+963935925081	t	t	2024-07-15 16:01:09.497217+03	f
4	pbkdf2_sha256$720000$exy964qDJRH3nWbktEeNsG$rmfNFdAU/Zbqd3Rtcp/d9zSvMPF9HdVRiWX+7e2wo8A=	\N	abo jood	sobh	abojood@gmail.com	+963935925081	t	t	2024-07-15 16:01:10.385144+03	f
6	pbkdf2_sha256$720000$P6vUnML3m5rPO5GouWIYCR$TP2iOF+eD+OsNCwDYfIWkMUjOwrjmh33lj64fr/OeTo=	\N	kinan	jbai	kinan@gmail.com	+9639345124552	f	t	2024-07-23 17:16:59.042973+03	f
5	pbkdf2_sha256$720000$FFKHwjGerymDOpFvvnEhB8$Fny2ivTsQEKh+bHYhh8CvN3bhmzekXVM3Bav2DDqVX8=	\N	aws	alsaad	aws@gmail.com	+963934534651	t	t	2024-07-23 15:40:40.222352+03	f
7	pbkdf2_sha256$720000$gSRIL4sbeGBghBvgp9oM8o$/5fDRx/yLmvHXa4BMFdFWm8QFVasKwU7naOV+HTD0/Q=	\N	maya	abo amad	maya@gmail.com	0934145962	f	t	2024-07-31 16:14:57.254738+03	f
8	pbkdf2_sha256$720000$4cKTXWClwohY9NXcpiVlOo$YbGSn6MX2sybA/jFrF6EV4glifUj4M7aTUVq465HsVQ=	\N	sakher	hatoum	shaker@gmail.com	+963934984651	f	t	2024-08-02 18:53:55.577277+03	f
9	pbkdf2_sha256$720000$bXum5pLIgh9DWTU0yPitqU$7HtY2znkqDmtgPntTw/GA3bofmo73beWvLZRwasY9B0=	\N	amer	hilal	amer@gmail.com	+963934454650	f	t	2024-08-02 19:01:47.666272+03	f
10	pbkdf2_sha256$720000$Gb7wwwKAVptjA0zLmuR7AT$DB7O501mKobZ/+qq85SJN2IdP8UaIa/NsOWLaIeuz9o=	\N	bashar	ballan	bashar@gmail.com	+963000454650	f	t	2024-08-03 20:55:37.3013+03	f
\.


--
-- Data for Name: accounts_emailverified; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accounts_emailverified (id, is_verified, verification_date, verfication_token, user_id, expire_date) FROM stdin;
1	t	2024-07-15 16:01:11.550672+03	YGNwKTECkiFoPDyLOcBPMRQc4i4QnXb2Q5Nl0n2v8QB--WVFUH3328hEjGypqdv4Tif7DHWf70hzvVCJh5i3Dw	2	2024-07-15 16:02:11.614555+03
2	t	2024-07-15 16:01:11.78035+03	9lQs_kCEizDdJzsiIFRht-ETipb8grxXNyQxcKJrLg_smnne_Whk5LAllbbr9FnNMBUrDdQ1rqenG7VaYbD9xw	3	2024-07-15 16:02:11.863299+03
3	t	2024-07-23 15:45:58.059082+03	Dj6qByKVC1KWcdeqpZtaZUM8eaOYIBGEgc-XHy-7QCdobH6sM_tLoOFsLxvtP4mq-u3_Sgkz-QrIe5_7XX3axQ	4	2024-07-23 15:51:17.288014+03
4	t	2024-07-23 17:19:11.883182+03	PsCt1TFCSnW_lBtM6ifBcR4xmHIrcFAPq1vQ9iJlZPlhEVQXXGGHBYwIkL4iaVkF2OotFHhEDZMTWhlk5DIqUg	5	2024-07-23 17:34:30.01302+03
5	t	2024-08-02 18:47:06.161532+03	vy4l-_xdk_oziFOBusUiHTqkP8yhTGX2CsPV1htBIgMXsbpOr9tOVRQKoY1I8Z8NWX-CkpYau82HAmXf6gA-Rw	6	2024-08-02 18:51:11.242578+03
6	t	2024-08-02 19:02:38.254183+03	cprcfKBhouGQCYZ-3zyb_mBF-xxd-1zjQZtVvSls-1qEgAPllOxx6CDMqFUdetqjBcKS_ZEsAcLopUqn9WkEgg	7	2024-08-02 19:05:22.902352+03
\.


--
-- Data for Name: locations_address; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.locations_address (id, street, village_city, state, country) FROM stdin;
1	\N	Joubar Municipality	Damascus Governorate	Syria
2	\N	Al-Tal	Rif Dimashq Governorate	Syria
3	Mohammad Al-Hamazani Lane	Barza Municipality	Damascus Governorate	Syria
4	\N	Al Mulayhah	Rif Dimashq Governorate	Syria
5	\N	Ad Dimas	Rif Dimashq Governorate	Syria
6	\N	Manīn	Rif Dimashq Governorate	Syria
7	\N	Rakhlah	Rif Dimashq Governorate	Syria
8	\N	Ayha	Beqaa Governorate	Lebanon
9	\N	Mhaidse	Beqaa Governorate	Lebanon
10	\N	Rashaya	Beqaa Governorate	Lebanon
11	\N	Biyad	Rif Dimashq Governorate	Syria
12	\N	`Assal al Ward	Rif Dimashq Governorate	Syria
13	Southern Bypass	Ash-Shaghour Municipality	Damascus Governorate	Syria
\.


--
-- Data for Name: locations_location; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.locations_location (id, latitude, longitude, address_id) FROM stdin;
1	33.510350000	36.319890000	1
2	33.590350000	36.379920000	2
3	33.552350000	36.309920000	3
4	33.490350000	36.379920000	4
5	33.590350000	36.079920000	5
6	33.690350000	36.279920000	6
7	33.490350000	35.979920000	7
8	33.480350000	35.919920000	8
9	33.550350000	35.819920000	9
10	33.450350000	35.899200000	10
11	33.450350000	36.399200000	11
12	33.850350000	36.399200000	12
13	33.492790000	36.317690000	13
\.


--
-- Data for Name: services_servicetype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.services_servicetype (id, type) FROM stdin;
1	food
2	DJservice
3	venue
5	photographer
6	entertainment
7	decoration
\.


--
-- Data for Name: services_service; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.services_service (id, name, description, service_provider_id, service_type_id, created_at, location_id, phone, updated_at, avg_rating) FROM stdin;
1	Grilling master	\N	2	1	2024-07-15 16:01:13.705117+03	1	+963947741054	2024-07-15 16:01:13.709114+03	0
7	DJ Malik	\N	3	2	2024-07-23 14:06:36.062094+03	2	963947741054	2024-07-31 20:19:36.470802+03	0
8	zvenue	\N	4	3	2024-07-23 15:54:16.928996+03	3	963947741054	2024-08-04 19:30:59.966343+03	0
9	Aws Forniture	\N	5	7	2024-07-23 17:42:25.151898+03	4	+963924574105	2024-08-05 14:56:24.799014+03	4.5
\.


--
-- Data for Name: accounts_otp; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accounts_otp (id, code, expire_date, is_verified, service_id, user_id) FROM stdin;
1	556055	2024-07-15 16:02:11.258481+03	t	\N	2
2	914754	2024-07-15 16:02:11.404418+03	t	\N	3
3	798162	2024-07-23 15:45:26.257187+03	t	\N	4
4	324290	2024-07-23 17:19:40.001505+03	t	\N	5
5	242805	2024-08-02 18:51:17.452882+03	t	\N	6
6	270894	2024-08-02 19:05:13.331597+03	t	\N	7
\.


--
-- Data for Name: accounts_passwordchangerequested; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accounts_passwordchangerequested (id, is_requested, user_id) FROM stdin;
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
6	authtoken	token
7	authtoken	tokenproxy
8	accounts	user
9	accounts	otp
10	accounts	passwordchangerequested
11	accounts	emailverified
12	events	eventtype
13	events	event
14	events	reservation
15	events	invitationcard
16	locations	address
17	locations	location
18	notifications	message
19	notifications	notification
20	photos	servicephotos
21	photos	foodphotos
22	photos	serviceprofilephoto
23	reviews	review
24	services	servicetype
25	services	serviceproviderapplication
26	services	service
27	services	foodtype
28	services	foodservice
29	services	food
30	services	foodservicefood
31	services	foodtypeservice
32	services	djservice
33	services	venue
34	services	photographerservice
35	services	decorationservice
36	services	entertainementservice
37	services	decore
39	services	booking
40	services	favoriteservice
41	videos	video
42	reports	reportreview
43	reports	reportservice
44	wallet	wallet
45	wallet	transaction
46	photos	mainfoodphoto
38	services	decoreventtype
47	photos	decorphotos
48	photos	maindecorphoto
49	services	decor
50	services	decorsreservation
51	services	decorsinreservation
52	services	order
53	services	foodinorder
54	services	decorinorder
55	services	servicereservation
56	wallet	centerwallet
57	services	reservation
58	wallet	userwallet
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
21	Can add Token	6	add_token
22	Can change Token	6	change_token
23	Can delete Token	6	delete_token
24	Can view Token	6	view_token
25	Can add Token	7	add_tokenproxy
26	Can change Token	7	change_tokenproxy
27	Can delete Token	7	delete_tokenproxy
28	Can view Token	7	view_tokenproxy
29	Can add user	8	add_user
30	Can change user	8	change_user
31	Can delete user	8	delete_user
32	Can view user	8	view_user
33	Can add otp	9	add_otp
34	Can change otp	9	change_otp
35	Can delete otp	9	delete_otp
36	Can view otp	9	view_otp
37	Can add password change requested	10	add_passwordchangerequested
38	Can change password change requested	10	change_passwordchangerequested
39	Can delete password change requested	10	delete_passwordchangerequested
40	Can view password change requested	10	view_passwordchangerequested
41	Can add email verified	11	add_emailverified
42	Can change email verified	11	change_emailverified
43	Can delete email verified	11	delete_emailverified
44	Can view email verified	11	view_emailverified
45	Can add event type	12	add_eventtype
46	Can change event type	12	change_eventtype
47	Can delete event type	12	delete_eventtype
48	Can view event type	12	view_eventtype
49	Can add event	13	add_event
50	Can change event	13	change_event
51	Can delete event	13	delete_event
52	Can view event	13	view_event
53	Can add reservation	14	add_reservation
54	Can change reservation	14	change_reservation
55	Can delete reservation	14	delete_reservation
56	Can view reservation	14	view_reservation
57	Can add invitation card	15	add_invitationcard
58	Can change invitation card	15	change_invitationcard
59	Can delete invitation card	15	delete_invitationcard
60	Can view invitation card	15	view_invitationcard
61	Can add address	16	add_address
62	Can change address	16	change_address
63	Can delete address	16	delete_address
64	Can view address	16	view_address
65	Can add location	17	add_location
66	Can change location	17	change_location
67	Can delete location	17	delete_location
68	Can view location	17	view_location
69	Can add message	18	add_message
70	Can change message	18	change_message
71	Can delete message	18	delete_message
72	Can view message	18	view_message
73	Can add notification	19	add_notification
74	Can change notification	19	change_notification
75	Can delete notification	19	delete_notification
76	Can view notification	19	view_notification
77	Can add service photos	20	add_servicephotos
78	Can change service photos	20	change_servicephotos
79	Can delete service photos	20	delete_servicephotos
80	Can view service photos	20	view_servicephotos
81	Can add food photos	21	add_foodphotos
82	Can change food photos	21	change_foodphotos
83	Can delete food photos	21	delete_foodphotos
84	Can view food photos	21	view_foodphotos
85	Can add service profile photo	22	add_serviceprofilephoto
86	Can change service profile photo	22	change_serviceprofilephoto
87	Can delete service profile photo	22	delete_serviceprofilephoto
88	Can view service profile photo	22	view_serviceprofilephoto
89	Can add review	23	add_review
90	Can change review	23	change_review
91	Can delete review	23	delete_review
92	Can view review	23	view_review
93	Can add service type	24	add_servicetype
94	Can change service type	24	change_servicetype
95	Can delete service type	24	delete_servicetype
96	Can view service type	24	view_servicetype
97	Can add service provider application	25	add_serviceproviderapplication
98	Can change service provider application	25	change_serviceproviderapplication
99	Can delete service provider application	25	delete_serviceproviderapplication
100	Can view service provider application	25	view_serviceproviderapplication
101	Can add service	26	add_service
102	Can change service	26	change_service
103	Can delete service	26	delete_service
104	Can view service	26	view_service
105	Can add food type	27	add_foodtype
106	Can change food type	27	change_foodtype
107	Can delete food type	27	delete_foodtype
108	Can view food type	27	view_foodtype
109	Can add food service	28	add_foodservice
110	Can change food service	28	change_foodservice
111	Can delete food service	28	delete_foodservice
112	Can view food service	28	view_foodservice
113	Can add food	29	add_food
114	Can change food	29	change_food
115	Can delete food	29	delete_food
116	Can view food	29	view_food
117	Can add food service food	30	add_foodservicefood
118	Can change food service food	30	change_foodservicefood
119	Can delete food service food	30	delete_foodservicefood
120	Can view food service food	30	view_foodservicefood
121	Can add food type service	31	add_foodtypeservice
122	Can change food type service	31	change_foodtypeservice
123	Can delete food type service	31	delete_foodtypeservice
124	Can view food type service	31	view_foodtypeservice
125	Can add dj service	32	add_djservice
126	Can change dj service	32	change_djservice
127	Can delete dj service	32	delete_djservice
128	Can view dj service	32	view_djservice
129	Can add venue	33	add_venue
130	Can change venue	33	change_venue
131	Can delete venue	33	delete_venue
132	Can view venue	33	view_venue
133	Can add photo grapher service	34	add_photographerservice
134	Can change photo grapher service	34	change_photographerservice
135	Can delete photo grapher service	34	delete_photographerservice
136	Can view photo grapher service	34	view_photographerservice
137	Can add decoration service	35	add_decorationservice
138	Can change decoration service	35	change_decorationservice
139	Can delete decoration service	35	delete_decorationservice
140	Can view decoration service	35	view_decorationservice
141	Can add entertainement service	36	add_entertainementservice
142	Can change entertainement service	36	change_entertainementservice
143	Can delete entertainement service	36	delete_entertainementservice
144	Can view entertainement service	36	view_entertainementservice
145	Can add decore	37	add_decore
146	Can change decore	37	change_decore
147	Can delete decore	37	delete_decore
148	Can view decore	37	view_decore
149	Can add decore type	38	add_decoretype
150	Can change decore type	38	change_decoretype
151	Can delete decore type	38	delete_decoretype
152	Can view decore type	38	view_decoretype
153	Can add booking	39	add_booking
154	Can change booking	39	change_booking
155	Can delete booking	39	delete_booking
156	Can view booking	39	view_booking
157	Can add favorite service	40	add_favoriteservice
158	Can change favorite service	40	change_favoriteservice
159	Can delete favorite service	40	delete_favoriteservice
160	Can view favorite service	40	view_favoriteservice
161	Can add video	41	add_video
162	Can change video	41	change_video
163	Can delete video	41	delete_video
164	Can view video	41	view_video
165	Can add report review	42	add_reportreview
166	Can change report review	42	change_reportreview
167	Can delete report review	42	delete_reportreview
168	Can view report review	42	view_reportreview
169	Can add report service	43	add_reportservice
170	Can change report service	43	change_reportservice
171	Can delete report service	43	delete_reportservice
172	Can view report service	43	view_reportservice
173	Can add wallet	44	add_wallet
174	Can change wallet	44	change_wallet
175	Can delete wallet	44	delete_wallet
176	Can view wallet	44	view_wallet
177	Can add transaction	45	add_transaction
178	Can change transaction	45	change_transaction
179	Can delete transaction	45	delete_transaction
180	Can view transaction	45	view_transaction
181	Can add main food photo	46	add_mainfoodphoto
182	Can change main food photo	46	change_mainfoodphoto
183	Can delete main food photo	46	delete_mainfoodphoto
184	Can view main food photo	46	view_mainfoodphoto
185	Can add decor photos	47	add_decorphotos
186	Can change decor photos	47	change_decorphotos
187	Can delete decor photos	47	delete_decorphotos
188	Can view decor photos	47	view_decorphotos
189	Can add main decor photo	48	add_maindecorphoto
190	Can change main decor photo	48	change_maindecorphoto
191	Can delete main decor photo	48	delete_maindecorphoto
192	Can view main decor photo	48	view_maindecorphoto
193	Can add decor event type	38	add_decoreventtype
194	Can change decor event type	38	change_decoreventtype
195	Can delete decor event type	38	delete_decoreventtype
196	Can view decor event type	38	view_decoreventtype
197	Can add decor	49	add_decor
198	Can change decor	49	change_decor
199	Can delete decor	49	delete_decor
200	Can view decor	49	view_decor
201	Can add decors reservation	50	add_decorsreservation
202	Can change decors reservation	50	change_decorsreservation
203	Can delete decors reservation	50	delete_decorsreservation
204	Can view decors reservation	50	view_decorsreservation
205	Can add decors in reservation	51	add_decorsinreservation
206	Can change decors in reservation	51	change_decorsinreservation
207	Can delete decors in reservation	51	delete_decorsinreservation
208	Can view decors in reservation	51	view_decorsinreservation
209	Can add order	52	add_order
210	Can change order	52	change_order
211	Can delete order	52	delete_order
212	Can view order	52	view_order
213	Can add food in order	53	add_foodinorder
214	Can change food in order	53	change_foodinorder
215	Can delete food in order	53	delete_foodinorder
216	Can view food in order	53	view_foodinorder
217	Can add decor in order	54	add_decorinorder
218	Can change decor in order	54	change_decorinorder
219	Can delete decor in order	54	delete_decorinorder
220	Can view decor in order	54	view_decorinorder
221	Can add service reservation	55	add_servicereservation
222	Can change service reservation	55	change_servicereservation
223	Can delete service reservation	55	delete_servicereservation
224	Can view service reservation	55	view_servicereservation
225	Can add center wallet	56	add_centerwallet
226	Can change center wallet	56	change_centerwallet
227	Can delete center wallet	56	delete_centerwallet
228	Can view center wallet	56	view_centerwallet
229	Can add reservation	57	add_reservation
230	Can change reservation	57	change_reservation
231	Can delete reservation	57	delete_reservation
232	Can view reservation	57	view_reservation
233	Can add user wallet	58	add_userwallet
234	Can change user wallet	58	change_userwallet
235	Can delete user wallet	58	delete_userwallet
236	Can view user wallet	58	view_userwallet
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
394241af0d9fa637dbd290dd734bece482a92e86	2024-07-15 16:01:08.779699+03	1
dbca40ccf3548ebb3a76b9bbe317bf849d6761ef	2024-07-15 16:01:09.447964+03	2
ce42baa06b3a4a474c9d8619fe0ac636a9602e25	2024-07-15 16:01:10.308194+03	3
bf9d8f623cc7f0632b20ac43d9a59a4168d423be	2024-07-15 16:01:11.029742+03	4
6181814cdb093c058ff6d09cf5e2656ab5701698	2024-07-23 15:40:41.033238+03	5
3b145318b39365778e19dabea6fb163ca8c5e09d	2024-07-23 17:16:59.826998+03	6
a006bfab0f320ee3662aaf92e3a325132c36b915	2024-07-31 16:14:58.014898+03	7
a4b605a455bcb5417772c0aafc498775cbcfd996	2024-08-02 18:53:56.30542+03	8
e587c41e5aaaf6034921ebd11e2385c4d5d6909a	2024-08-02 19:01:48.394568+03	9
db733ba2e8c18b4d5846836bbc1377a61f05a22f	2024-08-03 20:55:38.050291+03	10
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
26	accounts	0004_verifycode	2024-05-15 19:42:01.058644+03
27	accounts	0005_verifycode_status	2024-05-19 14:10:01.552609+03
28	locations	0001_initial	2024-05-22 18:54:20.957171+03
29	services	0001_initial	2024-05-22 18:54:23.22578+03
30	accounts	0006_otp_delete_verifycode	2024-05-22 18:54:23.958477+03
31	events	0001_initial	2024-05-22 18:54:25.383725+03
32	notifications	0001_initial	2024-05-22 18:54:26.308139+03
33	photos	0001_initial	2024-05-22 18:54:26.623334+03
34	reviews	0001_initial	2024-05-22 18:54:27.251133+03
35	accounts	0007_passwordchangerequested	2024-05-23 21:36:09.083245+03
36	services	0002_remove_service_hourly_rate_and_more	2024-05-24 15:54:27.515663+03
37	services	0003_foodtype_foodtypeservice	2024-05-27 20:05:13.536012+03
38	services	0004_remove_foodservice_cuisine_type_and_more	2024-05-29 18:11:28.656111+03
39	photos	0002_foodphotos_servicephotos_delete_photos	2024-05-29 18:11:29.41131+03
40	services	0005_food_gradients	2024-05-29 19:51:40.183015+03
41	services	0006_rename_gradients_food_ingredients	2024-05-29 19:53:53.729837+03
42	locations	0002_rename_city_address_place_name_and_more	2024-06-03 22:30:14.826224+03
43	locations	0003_rename_place_name_address_village_city	2024-06-03 22:40:18.847295+03
44	locations	0004_alter_address_country_alter_address_state_and_more	2024-06-04 16:02:25.140984+03
45	services	0007_decoration_venue_foodservice_area_limit_km_and_more	2024-06-05 00:21:28.54776+03
46	services	0008_alter_service_description	2024-06-05 01:07:08.041007+03
47	events	0002_event_other_type	2024-06-05 01:16:51.669774+03
48	photos	0003_alter_foodphotos_url_alter_servicephotos_url	2024-06-05 01:16:51.743132+03
49	services	0009_alter_foodservice_area_limit_km	2024-06-05 01:16:51.770117+03
50	videos	0001_initial	2024-06-05 01:16:52.151275+03
51	services	0010_alter_favoriteservice_unique_together	2024-06-05 02:40:19.738357+03
52	reviews	0002_alter_review_comment	2024-06-07 22:33:13.370754+03
53	reports	0001_initial	2024-06-07 22:33:15.19928+03
54	services	0011_decorationservice_entertainementservice_and_more	2024-06-07 22:33:17.03375+03
55	wallet	0001_initial	2024-06-07 22:33:17.742887+03
56	events	0003_invitationcard	2024-06-07 23:55:12.332851+03
57	accounts	0008_emailverified	2024-07-01 00:52:54.933437+03
58	accounts	0009_rename_code_emailverified_verfication_token_and_more	2024-07-01 09:39:37.957009+03
59	accounts	0010_emailverified_expire_date	2024-07-01 10:40:27.909605+03
60	accounts	0011_alter_emailverified_expire_date	2024-07-01 10:40:27.991833+03
61	accounts	0012_alter_emailverified_verification_date	2024-07-01 11:05:29.724838+03
62	accounts	0013_alter_emailverified_verification_date	2024-07-01 14:15:05.1642+03
63	accounts	0014_alter_emailverified_verification_date	2024-07-01 14:15:05.218119+03
64	photos	0004_rename_url_foodphotos_image_and_more	2024-07-01 14:15:05.26712+03
65	services	0012_alter_service_service_provider	2024-07-05 13:26:49.016493+03
66	photos	0005_alter_foodphotos_image_alter_servicephotos_image_and_more	2024-07-05 13:26:49.631062+03
67	services	0013_remove_decorationservice_hourly_rate_and_more	2024-07-16 13:24:49.297102+03
68	photos	0006_mainfoodphoto	2024-07-16 13:24:49.84446+03
69	services	0014_alter_djservice_hourly_rate	2024-07-23 14:03:56.729065+03
70	services	0015_alter_djservice_area_limit_km_and_more	2024-07-23 14:06:12.212072+03
71	services	0016_remove_venue_maximum_guests_and_more	2024-07-23 15:24:20.776837+03
73	services	0017_alter_servicetype_type	2024-07-23 23:33:46.498701+03
74	services	0018_remove_decoreventtype_decore_and_more	2024-07-23 23:36:45.588214+03
75	photos	0007_decorphotos_maindecorphoto	2024-07-23 23:36:45.98213+03
76	photos	0008_decorphotos_decor_maindecorphoto_decor_and_more	2024-07-23 23:36:46.632154+03
77	services	0019_decor_price	2024-07-24 11:06:27.992362+03
78	services	0020_alter_decor_hourly_rate_alter_decor_price	2024-07-24 11:28:40.668279+03
79	services	0021_rename_avialable_quantity_decor_available_quantity	2024-07-24 11:32:18.234165+03
80	photos	0009_alter_decorphotos_image	2024-07-25 18:35:26.856827+03
81	services	0022_service_avg_rating	2024-07-25 18:35:27.081005+03
82	reviews	0003_review_updated_at_alter_review_service	2024-07-25 18:35:27.212951+03
83	reviews	0004_review_unique_user_service	2024-07-25 18:50:12.48466+03
84	videos	0002_remove_video_description_remove_video_title	2024-07-31 09:37:18.341653+03
85	reports	0002_alter_reportservice_evidence	2024-07-31 16:09:33.305956+03
86	wallet	0002_remove_wallet_currency_alter_wallet_balance	2024-07-31 16:09:33.890027+03
87	photos	0010_remove_serviceprofilephoto_servicephoto_and_more	2024-07-31 16:59:30.902448+03
88	photos	0011_rename_image_serviceprofilephoto_servicephoto	2024-07-31 17:06:12.981837+03
89	wallet	0003_remove_transaction_timestamp_and_more	2024-08-01 00:18:03.234039+03
90	wallet	0004_transaction_wallet	2024-08-01 09:50:54.703783+03
91	events	0004_remove_event_other_type_alter_event_total_cost_and_more	2024-08-02 18:42:17.110049+03
92	services	0023_decorsreservation_decorsinreservation_order_and_more	2024-08-02 18:42:20.800192+03
93	wallet	0005_centerwallet_transaction_fee_and_more	2024-08-03 13:36:30.233446+03
94	services	0024_remove_decorsreservation_event_and_more	2024-08-03 18:53:31.404498+03
95	wallet	0006_transaction_order_transaction_reservation	2024-08-03 18:53:31.810568+03
96	wallet	0007_remove_wallet_user_remove_centerwallet_balance_and_more	2024-08-03 20:37:50.202222+03
97	services	0025_reservation_created_at_reservation_updated_at	2024-08-04 09:29:02.834508+03
98	services	0026_alter_reservation_status	2024-08-04 18:04:45.892786+03
99	wallet	0008_alter_transaction_transaction_type	2024-08-04 18:04:46.107977+03
100	services	0027_delete_decorinorder	2024-08-15 13:04:58.666173+03
101	services	0028_decorsinreservation_end_time	2024-08-15 13:07:51.403851+03
102	services	0029_order_created_at_order_due_date	2024-08-15 15:34:57.38823+03
103	services	0030_alter_order_status	2024-08-15 20:02:17.13149+03
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Data for Name: events_eventtype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.events_eventtype (id, name) FROM stdin;
2	birthday
3	wedding
4	gathering
5	graduation
6	party
7	Engagement party
8	anniversary
\.


--
-- Data for Name: events_event; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.events_event (id, name, start_time, end_time, total_cost, location_id, user_id, event_type_id) FROM stdin;
3	ramez graduation party	2024-09-11 23:00:00+03	2024-09-12 01:00:00+03	0.00	12	6	\N
4	graduation party	2024-08-20 15:00:00+03	2024-08-22 15:00:00+03	0.00	13	3	\N
\.


--
-- Data for Name: events_invitationcard; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.events_invitationcard (id, invitation, event_id) FROM stdin;
\.


--
-- Data for Name: notifications_message; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.notifications_message (id, message) FROM stdin;
\.


--
-- Data for Name: notifications_notification; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.notifications_notification (id, created_at, dest_id, message_id, source_id) FROM stdin;
\.


--
-- Data for Name: services_decorationservice; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.services_decorationservice (service_ptr_id, area_limit_km) FROM stdin;
9	50
\.


--
-- Data for Name: services_decor; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.services_decor (id, name, quantity, available_quantity, hourly_rate, description, decor_service_id, price) FROM stdin;
6	black roses	10000	10000	0.00	they suit for birthday parties	9	200.00
7	red chair	1000	1000	10.00		9	5000.00
\.


--
-- Data for Name: photos_decorphotos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.photos_decorphotos (id, image, uploaded_at, decor_id) FROM stdin;
2	pictures/decors/whtie_candles.png	2024-07-25 13:02:57.427842+03	7
3	pictures/decors/salmon.jpg	2024-07-25 13:07:07.097983+03	7
4	pictures/decors/dam.jfif	2024-07-31 12:46:50.141739+03	6
5	pictures/decors/soltan.jpg	2024-08-05 14:39:52.595247+03	6
6	pictures/decors/soltan_0LpQRWx.jpg	2024-08-05 14:54:03.907468+03	6
\.


--
-- Data for Name: services_foodtype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.services_foodtype (id, type) FROM stdin;
1	sea food
3	chicken
\.


--
-- Data for Name: services_food; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.services_food (id, name, price, food_type_id, ingredients) FROM stdin;
1	salmon	120000	1	
2	shawarma	35000	1	
3	grilled fish	35000	1	
4	fried salmon	50000	1	
7	broasted	200000	3	
\.


--
-- Data for Name: photos_foodphotos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.photos_foodphotos (id, image, uploaded_at, food_id) FROM stdin;
3	pictures/foods/salmon.jpg	2024-07-16 13:10:52.823844+03	1
4	pictures/foods/salmon2.jpg	2024-07-16 13:28:40.250397+03	1
6	pictures/foods/soltan.jpg	2024-08-05 13:44:13.439685+03	3
\.


--
-- Data for Name: photos_maindecorphoto; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.photos_maindecorphoto (id, decor_id, "decorPhoto_id") FROM stdin;
6	6	5
\.


--
-- Data for Name: photos_mainfoodphoto; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.photos_mainfoodphoto (id, food_id, "foodPhoto_id") FROM stdin;
2	1	4
5	3	6
\.


--
-- Data for Name: photos_servicephotos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.photos_servicephotos (id, image, uploaded_at, service_id) FROM stdin;
1	pictures/services/hartna.png	2024-07-27 18:44:04.27609+03	1
2	pictures/services/hartna2.png	2024-07-27 18:44:17.975629+03	1
3	pictures/services/expan.PNG	2024-07-27 18:46:42.81339+03	7
4	pictures/services/hartna2_bcNeSBq.jpg	2024-07-27 18:46:58.715853+03	7
5	pictures/services/hartna2_CTx2aDV.jpg	2024-07-27 18:48:12.159115+03	8
6	pictures/services/dara.png	2024-07-27 18:48:20.717822+03	8
7	pictures/services/dara_xlh5uCF.png	2024-07-27 18:49:37.62727+03	9
8	pictures/services/WIN_20211219_00_31_04_Pro.jpg	2024-07-27 18:50:03.4617+03	9
9	pictures/services/WIN_20211219_00_31_04_Pro_v84ITKf.jpg	2024-07-27 19:02:03.563002+03	8
10	pictures/services/nurikabe.PNG	2024-07-27 19:02:17.227442+03	8
11	pictures/services/happy.jpg	2024-07-27 19:02:35.39792+03	8
12	pictures/services/dog5.png	2024-07-27 19:02:53.046709+03	8
\.


--
-- Data for Name: photos_serviceprofilephoto; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.photos_serviceprofilephoto (id, service_id, "servicePhoto") FROM stdin;
6	1	pictures/services/profile_photos/dam.jfif
8	9	pictures/services/profile_photos/dam_vrrmwJI.jfif
\.


--
-- Data for Name: reviews_review; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reviews_review (id, rating, comment, created_at, service_id, user_id, updated_at) FROM stdin;
4	4	recommended	2024-07-25 18:49:03.333473+03	9	2	2024-07-25 18:49:03.333473+03
8	5	beatiful	2024-07-25 18:54:50.321475+03	9	3	2024-07-25 18:54:50.321475+03
\.


--
-- Data for Name: reports_reportreview; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reports_reportreview (id, reason, is_solved, reporter_id, review_id, solved_by_id) FROM stdin;
7	It is offensive for black people	t	2	8	1
\.


--
-- Data for Name: reports_reportservice; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reports_reportservice (id, reason, evidence, resolution, is_solved, created_at, updated_at, reporter_id, service_id, solved_by_id) FROM stdin;
1	they are liars	storage/reports/evidence/cat2.png	I want my money back	t	2024-07-27 09:44:47.423557+03	2024-07-27 09:47:08.586898+03	3	9	1
\.


--
-- Data for Name: services_decoreventtype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.services_decoreventtype (id, event_type_id, decor_id) FROM stdin;
5	2	6
6	3	6
7	2	7
8	3	7
\.


--
-- Data for Name: services_decorsinreservation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.services_decorsinreservation (id, quantity, start_time, price, decor_id, decors_reservation_id, end_time) FROM stdin;
4	10	2024-08-20 15:00:00+03	480	7	16	2024-08-22 15:00:00+03
5	10	2024-08-20 15:00:00+03	480	7	18	2024-08-22 15:00:00+03
\.


--
-- Data for Name: services_reservation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.services_reservation (id, start_time, end_time, status, cost, event_id, created_at, updated_at) FROM stdin;
12	2024-08-20 15:00:00+03	2024-08-20 17:00:00+03	Cancelled	200000.00	4	2024-08-14 23:43:51.784061+03	2024-08-14 23:46:33.76714+03
14	2024-08-20 15:00:00+03	2024-08-22 15:00:00+03	Pending	-480.00	4	2024-08-15 11:27:19.033904+03	2024-08-15 13:11:13.036616+03
15	2024-08-20 15:00:00+03	2024-08-22 15:00:00+03	Pending	480.00	4	2024-08-15 13:12:44.652436+03	2024-08-15 13:12:44.663366+03
16	2024-08-20 15:00:00+03	2024-08-22 15:00:00+03	Rejected	480.00	4	2024-08-15 13:20:34.885198+03	2024-08-15 13:33:44.914154+03
17	2024-08-20 15:00:00+03	2024-08-20 17:00:00+03	Pending	200000.00	4	2024-08-15 13:43:48.168898+03	2024-08-15 13:43:48.168898+03
18	2024-08-20 15:00:00+03	2024-08-22 15:00:00+03	Cancelled	480.00	4	2024-08-15 13:44:24.945964+03	2024-08-15 13:57:59.507007+03
\.


--
-- Data for Name: services_decorsreservation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.services_decorsreservation (decor_service_id, reservation_ptr_id) FROM stdin;
9	14
9	15
9	16
9	18
\.


--
-- Data for Name: services_djservice; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.services_djservice (service_ptr_id, music_genre, equipment_provided, hourly_rate, area_limit_km) FROM stdin;
7	western music	Drums,Guitars,Piano,Violin	\N	\N
\.


--
-- Data for Name: services_entertainementservice; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.services_entertainementservice (service_ptr_id, hourly_rate, area_limit_km) FROM stdin;
\.


--
-- Data for Name: services_favoriteservice; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.services_favoriteservice (id, user_id, service_id) FROM stdin;
\.


--
-- Data for Name: services_order; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.services_order (id, status, total_price, event_id, service_id, created_at, due_date) FROM stdin;
1	Pending	0	4	1	2024-08-15 15:34:56.431103+03	2024-08-20 15:00:00+03
4	Pending	0	4	1	2024-08-15 18:03:12.198065+03	2024-08-20 15:00:00+03
5	Pending	0	4	1	2024-08-15 18:03:37.039336+03	2024-08-20 15:00:00+03
6	Pending	2000000	4	1	2024-08-15 18:07:39.111385+03	2024-08-20 15:00:00+03
7	Pending	2000000	4	1	2024-08-15 18:19:19.640835+03	2024-08-20 15:00:00+03
8	Pending	2000000	4	1	2024-08-15 18:47:58.695926+03	2024-08-20 18:00:00+03
9	Pending	2000000	4	1	2024-08-15 18:50:27.180359+03	2024-08-20 18:00:00+03
10	Rejected	2000000	4	1	2024-08-15 18:51:19.139599+03	2024-08-20 18:00:00+03
11	Cancelled	2000000	4	1	2024-08-15 20:24:32.103785+03	2024-08-20 15:00:00+03
\.


--
-- Data for Name: services_foodinorder; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.services_foodinorder (id, quantity, price, food_id, order_id) FROM stdin;
1	10	2000000	7	6
2	10	2000000	7	7
3	10	2000000	7	8
4	10	2000000	7	9
5	10	2000000	7	10
6	10	2000000	7	11
\.


--
-- Data for Name: services_foodservice; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.services_foodservice (service_ptr_id, area_limit_km) FROM stdin;
1	\N
\.


--
-- Data for Name: services_foodservicefood; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.services_foodservicefood (id, food_id, "foodService_id") FROM stdin;
3	3	1
4	4	1
7	7	1
\.


--
-- Data for Name: services_foodtypeservice; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.services_foodtypeservice (id, "foodService_id", "foodType_id") FROM stdin;
2	1	1
5	1	3
\.


--
-- Data for Name: services_photographerservice; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.services_photographerservice (service_ptr_id, hourly_rate, area_limit_km) FROM stdin;
\.


--
-- Data for Name: services_serviceproviderapplication; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.services_serviceproviderapplication (id, "otherType", national_identity_front, national_identity_back, status, location_id, user_id, service_type_id, created_at, name, phone) FROM stdin;
1	\N	storage/pictures/identity/front_HO7aa2G.jpg	storage/pictures/identity/back_YyGZkKn.jpg	Approved	1	2	1	2024-07-15 16:01:13.610587+03	Grilling master	+963947741054
2	\N	storage/pictures/identity/idfront_tlaczPp.jpg	storage/pictures/identity/idback_VPOPed4.jpg	Approved	2	3	2	2024-07-23 13:50:15.653689+03	DJ Malik	963947741054
3	\N	storage/pictures/identity/idfront_rz4ioy9.jpg	storage/pictures/identity/idback_Q1hmL7G.jpg	Approved	3	4	3	2024-07-23 15:53:42.322935+03	Zvenue	963947741054
4	\N	storage/pictures/identity/idfront_nScgLL4.jpg	storage/pictures/identity/idback_LG6j7xw.jpg	Approved	4	5	7	2024-07-23 17:41:50.18602+03	Aws Forniture	+963924574105
\.


--
-- Data for Name: services_servicereservation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.services_servicereservation (service_id, reservation_ptr_id) FROM stdin;
8	12
8	17
\.


--
-- Data for Name: services_venue; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.services_venue (service_ptr_id, hourly_rate, capacity, amenities) FROM stdin;
8	100000.00	200	\N
\.


--
-- Data for Name: videos_video; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.videos_video (id, file, uploaded_at, service_id) FROM stdin;
\.


--
-- Data for Name: wallet_wallet; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.wallet_wallet (id, balance, created_at, updated_at) FROM stdin;
2	1050000.00	2024-07-31 16:23:55.304341+03	2024-08-15 23:27:56.008679+03
1	208488.00	2024-07-31 16:14:58.113705+03	2024-08-15 23:27:56.024942+03
6	0.00	2024-07-31 16:26:06.364674+03	2024-08-06 12:07:00.883477+03
7	0.00	2024-08-02 18:53:56.307738+03	2024-08-02 18:53:56.325296+03
8	0.00	2024-08-02 19:01:48.397047+03	2024-08-02 19:01:48.399001+03
9	0.00	2024-08-03 20:55:38.053288+03	2024-08-03 20:55:38.08067+03
3	2300000.00	2024-07-31 16:25:19.425802+03	2024-08-15 23:27:56.02894+03
4	300000.00	2024-07-31 16:25:37.956423+03	2024-08-14 23:46:33.694122+03
5	500.00	2024-07-31 16:25:50.369557+03	2024-08-15 13:57:59.500013+03
\.


--
-- Data for Name: wallet_centerwallet; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.wallet_centerwallet (wallet_ptr_id) FROM stdin;
1
\.


--
-- Data for Name: wallet_transaction; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.wallet_transaction (id, amount, transaction_type, made_at, receiver_id, sender_id, wallet_id, fee, order_id, reservation_id) FROM stdin;
81	300000.00	credit	2024-08-14 23:42:27.237866+03	\N	\N	3	\N	\N	\N
82	300000.00	credit	2024-08-14 23:43:25.273417+03	\N	\N	4	\N	\N	\N
83	-210000.00	debit	2024-08-14 23:43:51.846486+03	\N	\N	3	\N	\N	12
84	210000.00	credit	2024-08-14 23:43:51.851889+03	\N	\N	1	\N	\N	12
85	-210000.00	transfer	2024-08-14 23:43:51.852886+03	1	3	3	10000.00	\N	12
86	-105000.00	debit	2024-08-14 23:45:05.990913+03	\N	\N	4	\N	\N	12
87	105000.00	credit	2024-08-14 23:45:05.993912+03	\N	\N	1	\N	\N	12
88	-105000.00	transfer	2024-08-14 23:45:05.993912+03	1	4	4	5000.00	\N	12
89	-105000.00	debit	2024-08-14 23:46:33.692123+03	\N	\N	1	\N	\N	12
90	105000.00	credit	2024-08-14 23:46:33.69812+03	\N	\N	4	\N	\N	12
91	-105000.00	transfer	2024-08-14 23:46:33.700118+03	4	1	1	0.00	\N	12
92	-210000.00	debit	2024-08-14 23:46:33.761143+03	\N	\N	1	\N	\N	12
93	210000.00	credit	2024-08-14 23:46:33.763142+03	\N	\N	3	\N	\N	12
94	-210000.00	transfer	2024-08-14 23:46:33.764141+03	3	1	1	0.00	\N	12
95	-504.00	debit	2024-08-15 13:20:35.12505+03	\N	\N	3	\N	\N	16
96	504.00	credit	2024-08-15 13:20:35.131047+03	\N	\N	1	\N	\N	16
97	-504.00	transfer	2024-08-15 13:20:35.132046+03	1	3	3	24.00	\N	16
98	-504.00	debit	2024-08-15 13:33:44.89671+03	\N	\N	1	\N	\N	16
99	504.00	credit	2024-08-15 13:33:44.906705+03	\N	\N	3	\N	\N	16
100	-504.00	transfer	2024-08-15 13:33:44.908703+03	3	1	1	0.00	\N	16
101	-210000.00	debit	2024-08-15 13:43:48.18189+03	\N	\N	3	\N	\N	17
102	210000.00	credit	2024-08-15 13:43:48.186887+03	\N	\N	1	\N	\N	17
103	-210000.00	transfer	2024-08-15 13:43:48.187886+03	1	3	3	10000.00	\N	17
104	-504.00	debit	2024-08-15 13:44:24.963417+03	\N	\N	3	\N	\N	18
105	504.00	credit	2024-08-15 13:44:24.966415+03	\N	\N	1	\N	\N	18
106	-504.00	transfer	2024-08-15 13:44:24.967418+03	1	3	3	24.00	\N	18
107	500.00	credit	2024-08-15 13:48:35.127426+03	\N	\N	5	\N	\N	\N
108	-252.00	debit	2024-08-15 13:48:59.140866+03	\N	\N	5	\N	\N	18
109	252.00	credit	2024-08-15 13:48:59.144296+03	\N	\N	1	\N	\N	18
110	-252.00	transfer	2024-08-15 13:48:59.145295+03	1	5	5	12.00	\N	18
111	-504.00	debit	2024-08-15 13:57:05.383344+03	\N	\N	1	\N	\N	18
112	504.00	credit	2024-08-15 13:57:05.387341+03	\N	\N	3	\N	\N	18
113	-504.00	transfer	2024-08-15 13:57:05.389339+03	3	1	1	0.00	\N	18
114	-504.00	debit	2024-08-15 13:57:07.737245+03	\N	\N	1	\N	\N	18
115	504.00	credit	2024-08-15 13:57:07.739243+03	\N	\N	3	\N	\N	18
116	-504.00	transfer	2024-08-15 13:57:07.740242+03	3	1	1	0.00	\N	18
117	-504.00	debit	2024-08-15 13:57:17.342057+03	\N	\N	1	\N	\N	18
118	504.00	credit	2024-08-15 13:57:17.348054+03	\N	\N	3	\N	\N	18
119	-504.00	transfer	2024-08-15 13:57:17.350053+03	3	1	1	0.00	\N	18
120	-504.00	debit	2024-08-15 13:57:59.486021+03	\N	\N	1	\N	\N	18
121	504.00	credit	2024-08-15 13:57:59.490019+03	\N	\N	3	\N	\N	18
122	-504.00	transfer	2024-08-15 13:57:59.491017+03	3	1	1	0.00	\N	18
123	-252.00	debit	2024-08-15 13:57:59.500013+03	\N	\N	1	\N	\N	18
124	252.00	credit	2024-08-15 13:57:59.502012+03	\N	\N	5	\N	\N	18
125	-252.00	transfer	2024-08-15 13:57:59.504011+03	5	1	1	0.00	\N	18
126	200000.00	credit	2024-08-15 18:14:00.833792+03	\N	\N	3	\N	\N	\N
127	8000.00	credit	2024-08-15 18:49:04.311527+03	\N	\N	3	\N	\N	\N
128	488.00	credit	2024-08-15 18:50:10.073756+03	\N	\N	3	\N	\N	\N
129	2000000.00	credit	2024-08-15 18:51:13.391321+03	\N	\N	3	\N	\N	\N
130	-2100000.00	debit	2024-08-15 18:51:19.230377+03	\N	\N	3	\N	10	\N
131	2100000.00	credit	2024-08-15 18:51:19.265856+03	\N	\N	1	\N	10	\N
132	-2100000.00	transfer	2024-08-15 18:51:19.266855+03	1	3	3	100000.00	10	\N
133	-2100000.00	debit	2024-08-15 20:11:57.912586+03	\N	\N	1	\N	10	\N
134	2100000.00	credit	2024-08-15 20:11:57.947388+03	\N	\N	3	\N	10	\N
135	-2100000.00	transfer	2024-08-15 20:11:57.948388+03	3	1	1	0.00	10	\N
136	-2100000.00	debit	2024-08-15 20:24:32.430695+03	\N	\N	3	\N	11	\N
137	2100000.00	credit	2024-08-15 20:24:32.437693+03	\N	\N	1	\N	11	\N
138	-2100000.00	transfer	2024-08-15 20:24:32.439691+03	1	3	3	100000.00	11	\N
139	-1050000.00	debit	2024-08-15 20:30:30.929688+03	\N	\N	2	\N	11	\N
140	1050000.00	credit	2024-08-15 20:30:30.934687+03	\N	\N	1	\N	11	\N
141	-1050000.00	transfer	2024-08-15 20:30:30.936016+03	1	2	2	50000.00	11	\N
142	-1050000.00	debit	2024-08-15 23:27:55.922598+03	\N	\N	1	\N	11	\N
143	1050000.00	credit	2024-08-15 23:27:56.010678+03	\N	\N	2	\N	11	\N
144	-1050000.00	transfer	2024-08-15 23:27:56.011674+03	2	1	1	0.00	11	\N
145	-2100000.00	debit	2024-08-15 23:27:56.027942+03	\N	\N	1	\N	11	\N
146	2100000.00	credit	2024-08-15 23:27:56.03194+03	\N	\N	3	\N	11	\N
147	-2100000.00	transfer	2024-08-15 23:27:56.032939+03	3	1	1	0.00	11	\N
\.


--
-- Data for Name: wallet_userwallet; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.wallet_userwallet (wallet_ptr_id, user_id) FROM stdin;
5	5
7	7
8	8
9	10
2	2
3	3
6	6
4	4
\.


--
-- Name: accounts_emailverified_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_emailverified_id_seq', 6, true);


--
-- Name: accounts_otp_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_otp_id_seq', 6, true);


--
-- Name: accounts_passwordchangerequested_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_passwordchangerequested_id_seq', 1, false);


--
-- Name: accounts_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_user_groups_id_seq', 1, false);


--
-- Name: accounts_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_user_id_seq', 10, true);


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

SELECT pg_catalog.setval('public.auth_permission_id_seq', 236, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 58, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 103, true);


--
-- Name: events_event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.events_event_id_seq', 4, true);


--
-- Name: events_eventtype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.events_eventtype_id_seq', 8, true);


--
-- Name: events_invitationcard_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.events_invitationcard_id_seq', 1, false);


--
-- Name: locations_address_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.locations_address_id_seq', 13, true);


--
-- Name: locations_location_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.locations_location_id_seq', 13, true);


--
-- Name: notifications_message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.notifications_message_id_seq', 1, false);


--
-- Name: notifications_notification_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.notifications_notification_id_seq', 1, false);


--
-- Name: photos_decorphotos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.photos_decorphotos_id_seq', 6, true);


--
-- Name: photos_foodphotos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.photos_foodphotos_id_seq', 6, true);


--
-- Name: photos_maindecorphoto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.photos_maindecorphoto_id_seq', 6, true);


--
-- Name: photos_mainfoodphoto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.photos_mainfoodphoto_id_seq', 5, true);


--
-- Name: photos_servicephotos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.photos_servicephotos_id_seq', 12, true);


--
-- Name: photos_serviceprofilephoto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.photos_serviceprofilephoto_id_seq', 8, true);


--
-- Name: reports_reportreview_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reports_reportreview_id_seq', 7, true);


--
-- Name: reports_reportservice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reports_reportservice_id_seq', 1, true);


--
-- Name: reviews_review_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reviews_review_id_seq', 9, true);


--
-- Name: services_decor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.services_decor_id_seq', 8, true);


--
-- Name: services_decoretype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.services_decoretype_id_seq', 8, true);


--
-- Name: services_decorsinreservation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.services_decorsinreservation_id_seq', 5, true);


--
-- Name: services_favoriteservice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.services_favoriteservice_id_seq', 1, false);


--
-- Name: services_food_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.services_food_id_seq', 7, true);


--
-- Name: services_foodinorder_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.services_foodinorder_id_seq', 6, true);


--
-- Name: services_foodservicefood_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.services_foodservicefood_id_seq', 7, true);


--
-- Name: services_foodtype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.services_foodtype_id_seq', 3, true);


--
-- Name: services_foodtypeservice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.services_foodtypeservice_id_seq', 5, true);


--
-- Name: services_order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.services_order_id_seq', 11, true);


--
-- Name: services_reservation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.services_reservation_id_seq', 18, true);


--
-- Name: services_service_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.services_service_id_seq', 9, true);


--
-- Name: services_serviceproviderapplication_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.services_serviceproviderapplication_id_seq', 4, true);


--
-- Name: services_servicetype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.services_servicetype_id_seq', 7, true);


--
-- Name: videos_video_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.videos_video_id_seq', 1, true);


--
-- Name: wallet_transaction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.wallet_transaction_id_seq', 147, true);


--
-- Name: wallet_wallet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.wallet_wallet_id_seq', 9, true);


--
-- PostgreSQL database dump complete
--

