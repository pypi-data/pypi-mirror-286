# your_package/main.py

import secrets
import os
import inquirer
import json
from urllib.parse import urlparse


def generate_secret():
    return secrets.token_hex(64)


def write_to_env_file(**kwargs):
    env_file = ".env"
    backup_env_file = ".env.backup"

    # Create a backup of the existing .env file
    if os.path.exists(env_file):
        os.rename(env_file, backup_env_file)

    with open(env_file, "w") as file:
        for key, value in kwargs.items():
            file.write(f"{key}={value}\n")

    # Generate .env.example
    with open(".env.example", "w") as file:
        for key in kwargs.keys():
            file.write(f"{key}=\n")


def save_template(template_name, env_vars):
    with open(f"{template_name}.json", "w") as file:
        json.dump(env_vars, file)


def load_template(template_name):
    with open(f"{template_name}.json", "r") as file:
        return json.load(file)


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def validate_url(answers, current):
    if current == "" or is_valid_url(current):
        return True
    else:
        raise inquirer.errors.ValidationError(
            current, reason="Invalid URL format. Please enter a valid URL."
        )


def validate_integer(answers, current):
    if current.isdigit():
        return True
    else:
        raise inquirer.errors.ValidationError(
            current, reason="Invalid number format. Please enter a valid integer."
        )


def prompt_custom_vars(env_vars):
    while True:
        custom_var_prompt = [
            inquirer.Text(
                'key', message="Enter the environment variable name (or type 'done' to finish):"),
        ]
        custom_var_answer = inquirer.prompt(custom_var_prompt)

        if custom_var_answer['key'].lower() == 'done':
            break

        custom_var_value_prompt = [
            inquirer.Text('value', message=f"Enter the value for {
                          custom_var_answer['key']}:"),
        ]
        custom_var_value_answer = inquirer.prompt(custom_var_value_prompt)

        env_vars[custom_var_answer['key']] = custom_var_value_answer['value']


def main():
    try:
        # Print the Python logo and a welcoming message
        print(r"""
          ____        _   _
         |  _ \ _   _| |_| |__   ___  _ __
         | |_) | | | | __| '_ \ / _ \| '_ \
         |  __/| |_| | |_| | | | (_) | | | |
         |_|    \__, |\__|_| |_|\___/|_| |_|
                |___/
        """)
        print("Welcome to the Python Environment Configuration Tool!")

        stack_questions = [
            inquirer.List('stack',
                          message="What kind of Python stack are you using?",
                          choices=['Flask', 'Django', 'FastAPI'],
                          ),
        ]
        stack_answer = inquirer.prompt(stack_questions)

        if not stack_answer:
            print("Cancelled by user.")
            return

        env_specific_questions = [
            inquirer.List('env', message="Which environment are you configuring?", choices=[
                          'development', 'testing', 'production']),
        ]
        env_specific_answer = inquirer.prompt(env_specific_questions)

        if not env_specific_answer:
            print("Cancelled by user.")
            return

        auth_system_question = [
            inquirer.Confirm(
                'use_auth', message="Are you building an authentication system?", default=True),
        ]

        auth_system_answer = inquirer.prompt(auth_system_question)

        if not auth_system_answer:
            print("Cancelled by user.")
            return

        auth_answers = {}
        if auth_system_answer['use_auth']:
            auth_questions = [
                inquirer.List('auth_type', message="What type of authentication are you using?", choices=[
                              'JWT', 'Session-based']),
                inquirer.Confirm(
                    'use_refresh_token', message="Do you need access and refresh tokens?", default=True),
            ]
            auth_answers = inquirer.prompt(auth_questions)

            if not auth_answers:
                print("Cancelled by user.")
                return

        feature_questions = [
            inquirer.Confirm(
                'use_email', message="Will your application use email protocols?", default=False),
            inquirer.Confirm(
                'use_redis', message="Will your application use Redis?", default=False),
            inquirer.Confirm(
                'use_sql', message="Will your application use SQL databases?", default=True),
            inquirer.Confirm(
                'use_nosql', message="Will your application use NoSQL databases?", default=False),
            inquirer.Confirm(
                'use_elasticsearch', message="Will your application use Elasticsearch?", default=False),
        ]

        feature_answers = inquirer.prompt(feature_questions)

        if not feature_answers:
            print("Cancelled by user.")
            return

        flask_questions = [
            inquirer.List('flask_env', message="Flask environment",
                          choices=['development', 'production']),
            inquirer.Text('secret_key', message="Flask secret key",
                          default=generate_secret()),
            inquirer.Confirm(
                'debug', message="Enable debug mode?", default=False),
            inquirer.Text('cors_origins', message="CORS origins",
                          validate=validate_url),
        ]

        django_questions = [
            inquirer.Text('django_settings_module',
                          message="Django settings module", default="myproject.settings"),
            inquirer.Text('secret_key', message="Django secret key",
                          default=generate_secret()),
            inquirer.Confirm(
                'debug', message="Enable debug mode?", default=False),
            inquirer.Text('allowed_hosts', message="Allowed hosts"),
        ]

        fastapi_questions = [
            inquirer.Text('secret_key', message="FastAPI secret key",
                          default=generate_secret()),
            inquirer.Confirm(
                'debug', message="Enable debug mode?", default=False),
            inquirer.Text('allowed_hosts', message="Allowed hosts"),
        ]

        db_questions = [
            inquirer.Text('db_name', message="Database name"),
            inquirer.Text('db_user', message="Database user"),
            inquirer.Password('db_password', message="Database password"),
            inquirer.Text('db_host', message="Database host"),
            inquirer.Text('db_port', message="Database port",
                          validate=validate_integer),
            inquirer.Text('db_dialect', message="Database dialect"),
        ]

        nosql_questions = [
            inquirer.List('nosql_type', message="Which NoSQL database are you using?", choices=[
                          'MongoDB', 'Cassandra']),
        ]

        mongodb_questions = [
            inquirer.Text('mongodb_uri', message="MongoDB URI",
                          validate=validate_url),
        ]

        cassandra_questions = [
            inquirer.Text('cassandra_contact_points',
                          message="Cassandra contact points (comma-separated hostnames or IPs)"),
            inquirer.Text('cassandra_keyspace', message="Cassandra keyspace"),
        ]

        elasticsearch_questions = [
            inquirer.Text('elasticsearch_url',
                          message="Elasticsearch URL", validate=validate_url),
            inquirer.Text('elasticsearch_index',
                          message="Elasticsearch index"),
        ]

        env_vars = {}

        if stack_answer['stack'] == 'Flask':
            flask_answers = inquirer.prompt(flask_questions)
            if not flask_answers:
                print("Cancelled by user.")
                return

            env_vars.update({
                "FLASK_ENV": flask_answers['flask_env'],
                "SECRET_KEY": flask_answers['secret_key'],
                "DEBUG": str(flask_answers['debug']),
                "CORS_ORIGINS": flask_answers['cors_origins'],
            })

            if feature_answers['use_sql']:
                sqlalchemy_question = [
                    inquirer.Text(
                        'sqlalchemy_database_uri', message="SQLAlchemy database URI (leave empty if providing separate DB parameters)", validate=validate_url),
                ]
                sqlalchemy_answer = inquirer.prompt(sqlalchemy_question)
                if sqlalchemy_answer and sqlalchemy_answer['sqlalchemy_database_uri']:
                    env_vars["SQLALCHEMY_DATABASE_URI"] = sqlalchemy_answer['sqlalchemy_database_uri']
                else:
                    db_answers = inquirer.prompt(db_questions)
                    if not db_answers:
                        print("Cancelled by user.")
                        return
                    env_vars.update({
                        "DB_NAME": db_answers['db_name'],
                        "DB_USER": db_answers['db_user'],
                        "DB_PASSWORD": db_answers['db_password'],
                        "DB_HOST": db_answers['db_host'],
                        "DB_PORT": db_answers['db_port'],
                        "DB_DIALECT": db_answers['db_dialect'],
                    })

        elif stack_answer['stack'] == 'Django':
            django_answers = inquirer.prompt(django_questions)
            if not django_answers:
                print("Cancelled by user.")
                return

            env_vars.update({
                "DJANGO_SETTINGS_MODULE": django_answers['django_settings_module'],
                "SECRET_KEY": django_answers['secret_key'],
                "DEBUG": str(django_answers['debug']),
                "ALLOWED_HOSTS": django_answers['allowed_hosts'],
            })

            if feature_answers['use_sql']:
                django_db_question = [
                    inquirer.Text(
                        'database_url', message="Database URL (leave empty if providing separate DB parameters)", validate=validate_url),
                ]
                django_db_answer = inquirer.prompt(django_db_question)
                if django_db_answer and django_db_answer['database_url']:
                    env_vars["DATABASE_URL"] = django_db_answer['database_url']
                else:
                    db_answers = inquirer.prompt(db_questions)
                    if not db_answers:
                        print("Cancelled by user.")
                        return
                    env_vars.update({
                        "DB_NAME": db_answers['db_name'],
                        "DB_USER": db_answers['db_user'],
                        "DB_PASSWORD": db_answers['db_password'],
                        "DB_HOST": db_answers['db_host'],
                        "DB_PORT": db_answers['db_port'],
                        "DB_DIALECT": db_answers['db_dialect'],
                    })

        elif stack_answer['stack'] == 'FastAPI':
            fastapi_answers = inquirer.prompt(fastapi_questions)
            if not fastapi_answers:
                print("Cancelled by user.")
                return

            env_vars.update({
                "SECRET_KEY": fastapi_answers['secret_key'],
                "DEBUG": str(fastapi_answers['debug']),
                "ALLOWED_HOSTS": fastapi_answers['allowed_hosts'],
            })

            if feature_answers['use_sql']:
                fastapi_db_question = [
                    inquirer.Text(
                        'database_url', message="Database URL (leave empty if providing separate DB parameters)", validate=validate_url),
                ]
                fastapi_db_answer = inquirer.prompt(fastapi_db_question)
                if fastapi_db_answer and fastapi_db_answer['database_url']:
                    env_vars["DATABASE_URL"] = fastapi_db_answer['database_url']
                else:
                    db_answers = inquirer.prompt(db_questions)
                    if not db_answers:
                        print("Cancelled by user.")
                        return
                    env_vars.update({
                        "DB_NAME": db_answers['db_name'],
                        "DB_USER": db_answers['db_user'],
                        "DB_PASSWORD": db_answers['db_password'],
                        "DB_HOST": db_answers['db_host'],
                        "DB_PORT": db_answers['db_port'],
                        "DB_DIALECT": db_answers['db_dialect'],
                    })

        if auth_system_answer['use_auth'] and auth_answers.get('auth_type') == 'JWT':
            env_vars["ACCESS_TOKEN_SECRET"] = generate_secret()
            if auth_answers['use_refresh_token']:
                env_vars["REFRESH_TOKEN_SECRET"] = generate_secret()

        if feature_answers['use_email']:
            email_questions = [
                inquirer.Text('email_host', message="Email server host"),
                inquirer.Text(
                    'email_port', message="Email server port", validate=validate_integer),
                inquirer.Text('email_user', message="Email server username"),
                inquirer.Password('email_password',
                                  message="Email server password"),
            ]
            email_answers = inquirer.prompt(email_questions)
            if not email_answers:
                print("Cancelled by user.")
                return
            env_vars.update({
                "EMAIL_HOST": email_answers['email_host'],
                "EMAIL_PORT": email_answers['email_port'],
                "EMAIL_USER": email_answers['email_user'],
                "EMAIL_PASSWORD": email_answers['email_password'],
            })

        if feature_answers['use_redis']:
            redis_questions = [
                inquirer.Text('redis_host', message="Redis host"),
                inquirer.Text('redis_port', message="Redis port",
                              validate=validate_integer),
                inquirer.Text(
                    'redis_password', message="Redis password (leave empty if not applicable)"),
            ]
            redis_answers = inquirer.prompt(redis_questions)
            if not redis_answers:
                print("Cancelled by user.")
                return
            env_vars.update({
                "REDIS_HOST": redis_answers['redis_host'],
                "REDIS_PORT": redis_answers['redis_port'],
                "REDIS_PASSWORD": redis_answers['redis_password'],
            })

        if feature_answers['use_nosql']:
            nosql_answers = inquirer.prompt(nosql_questions)
            if not nosql_answers:
                print("Cancelled by user.")
                return
            if nosql_answers['nosql_type'] == 'MongoDB':
                mongodb_answers = inquirer.prompt(mongodb_questions)
                if not mongodb_answers:
                    print("Cancelled by user.")
                    return
                env_vars.update({
                    "MONGODB_URI": mongodb_answers['mongodb_uri'],
                })
            elif nosql_answers['nosql_type'] == 'Cassandra':
                cassandra_answers = inquirer.prompt(cassandra_questions)
                if not cassandra_answers:
                    print("Cancelled by user.")
                    return
                env_vars.update({
                    "CASSANDRA_CONTACT_POINTS": cassandra_answers['cassandra_contact_points'],
                    "CASSANDRA_KEYSPACE": cassandra_answers['cassandra_keyspace'],
                })

        if feature_answers['use_elasticsearch']:
            elasticsearch_answers = inquirer.prompt(elasticsearch_questions)
            if not elasticsearch_answers:
                print("Cancelled by user.")
                return
            env_vars.update({
                "ELASTICSEARCH_URL": elasticsearch_answers['elasticsearch_url'],
                "ELASTICSEARCH_INDEX": elasticsearch_answers['elasticsearch_index'],
            })

        # Prompt for custom environment variables
        prompt_custom_vars(env_vars)

        # Show detailed summary and confirm
        summary_prompt = [
            inquirer.Confirm(
                'confirm', message="Here is the summary of your configuration. Do you want to write it to the .env file?", default=True),
        ]
        print("\nConfiguration Summary:")
        for key, value in env_vars.items():
            print(f"{key}={value}")
        summary_answer = inquirer.prompt(summary_prompt)

        if summary_answer and summary_answer['confirm']:
            write_to_env_file(**env_vars)
            print(".env variables have been written successfully.")
        else:
            print("Configuration aborted. No changes were made.")

        # Save template if required
        template_questions = [
            inquirer.Confirm(
                'save_template', message="Do you want to save this configuration as a template?", default=False),
        ]
        template_answer = inquirer.prompt(template_questions)
        if template_answer and template_answer['save_template']:
            template_name_question = [
                inquirer.Text('template_name',
                              message="Enter the template name:"),
            ]
            template_name_answer = inquirer.prompt(template_name_question)
            save_template(template_name_answer['template_name'], env_vars)
            print(f"Configuration template '{
                  template_name_answer['template_name']}' saved successfully.")

    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting gracefully.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
