workspace_creation_event_types = [
    'workspace_creation_create_workspace_directory',
    'workspace_creation_create_projects_directory',
    'workspace_creation_write_workspace_dockerfile',
    'workspace_creation_write_workspace_docker_compose_file',
    'workspace_creation_write_alembic_ini_to_workspace_directory',
    'workspace_creation_write_alembic_env_to_workspace_directory',
    'workspace_creation_write_env_to_workspace_directory',
    'workspace_creation_copy_initial_sqlalchemy_models_to_workspace_directory',
    'workspace_creation_build_workspace_pgadmin_container',
    'workspace_creation_build_workspace_postgres_container',
    'workspace_creation_build_workspace_alembic_worker_container',
    'workspace_creation_start_workspace_pgadmin_container',
    'workspace_creation_start_workspace_postgres_container',
    'workspace_creation_start_workspace_alembic_worker_container',
    'workspace_creation_wait_for_workspace_pgadmin_container',
    'workspace_creation_wait_for_workspace_postgres_container',
    'workspace_creation_wait_for_workspace_alembic_worker_container',
    'workspace_creation_run_alembic_init_migration',
    'workspace_creation_run_alembic_upgrade_head',
    'workspace_creation_run_alembic_revision_autogenerate',
    'workspace_creation_run_alembic_tail',
    'workspace_creation_run_alembic_migration',
    'workspace_creation_run_alembic_upgrade',
    'workspace_creation_run_alembic_downgrade',
    'workspace_creation_run_alembic_history',
    'workspace_creation_run_alembic_current',
    'workspace_creation_run_alembic_stamp',
]

database_event_types = [
    'database_creation_create_database'
    'database_creation_create_table',
    'database_creation_create_column'
]

project_creation_event_types = [
    'project_creation_create_project_directory',
    'project_creation_write_project_gitignore_file',
    'project_creation_write_project_setup_file',
    'project_creation_write_project_dockerfile',
    'project_creation_write_project_docker_compose_file',
    'project_creation_initialize_git_repository',
    'project_creation_create_github_repository',
    'project_creation_set_github_repository_remote',
    'project_creation_push_to_github_repository',
    'project_creation_write_main_file',
    'project_creation_write_github_actions_file',
    'project_creation_create_docs_directory',
    'project_creation_write_readme_file',
    'project_creation_write_pytest_command_tests',
    'project_creation_write_fresh_library_installation_tests',
    'project_creation_login_to_pypi',
    'project_creation_create_pypi_package',
    'project_creation_release_pypi_package'
]


event_types = workspace_creation_event_types + database_event_types + project_creation_event_types
