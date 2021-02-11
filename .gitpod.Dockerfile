FROM gitpod/workspace-postgres

RUN echo 'alias manage="python /workspace/ledger/manage.py"' >> ~/.bashrc
