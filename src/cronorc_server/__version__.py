__version__ = "0.post4"
__git_commiter_name__ = "Itai Shirav"
__git_commiter_email__ = "itais@infinidat.com"
__git_branch__ = 'develop'
__git_remote_tracking_branch__ = 'origin/develop'
__git_remote_url__ = 'git@git.infinidat.com:host-opensource/cronorc.git'
__git_head_hash__ = '1f5b0009d5116802af3b58cb83a000bffb518097'
__git_head_subject__ = 'Add navbar'
__git_head_message__ = ''
__git_dirty_diff__ = 'diff --git a/buildout.cfg b/buildout.cfg\nindex 9b8c0d1..2d95128 100644\n--- a/buildout.cfg\n+++ b/buildout.cfg\n@@ -11,6 +11,7 @@ company = Infinidat\n namespace_packages = []\n install_requires = [\n \t\'Django==2.2.9\',\n+    \'django-choices\',\n \t\'gunicorn\',\n \t\'setuptools\'\n \t]\ndiff --git a/src/cronorc_server/main/templates/home.html b/src/cronorc_server/main/templates/home.html\nindex e5f7d3a..e91fec2 100644\n--- a/src/cronorc_server/main/templates/home.html\n+++ b/src/cronorc_server/main/templates/home.html\n@@ -12,8 +12,8 @@\n                 <th>Date</th>\n                 <th>Host</th>\n                 <th>Command</th>\n+                <th>Result</th>\n                 <th>Elapsed</th>\n-                <th>Status</th>\n         </thead>\n         <tbody>\n             {%% for e in executions %%}\n@@ -21,12 +21,12 @@\n                     <td>{{ e.start|date:"SHORT_DATETIME_FORMAT" }}</td>\n                     <td>{{ e.job.hostname }} [{{ e.job.ip }}]</td>\n                     <td>{{ e.job.command }}</td>\n-                    <td>{{ e.elapsed|intcomma }}ms</td>\n                     {%% if e.success %%}\n                         <td>success</td>\n                     {%% else %%}\n                         <td class="text-danger">failure</td>\n                     {%% endif %%}\n+                    <td>{{ e.elapsed|intcomma }}ms</td>\n                 </tr>\n             {%% endfor %%}\n         </tbody>\n'
__git_commit_date__ = '2020-01-25 19:50:30'
