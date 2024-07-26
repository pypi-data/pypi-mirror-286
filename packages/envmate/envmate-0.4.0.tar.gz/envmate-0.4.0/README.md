
# envmate

`envmate` is an interactive command-line tool designed to simplify the process of configuring environment variables for your Python projects. It provides a user-friendly interface to set up `.env` files for various Python frameworks such as Flask, Django, and FastAPI, as well as configure database connections, authentication systems, and other essential settings.

## Features

- **Interactive Setup**: Guides you through the process of setting up environment variables with an easy-to-use interactive prompt.
- **Support for Multiple Frameworks**: Configure environment variables for Flask, Django, and FastAPI projects.
- **Database Configuration**: Supports both SQL (PostgreSQL, MySQL) and NoSQL (MongoDB, Cassandra) databases.
- **Authentication Setup**: Allows you to set up JWT or session-based authentication, including access and refresh tokens.
- **Custom Environment Variables**: Add custom environment variables specific to your project's needs.
- **Configuration Templates**: Save and reuse configuration templates to streamline the setup process for future projects.
- **Environment-specific Settings**: Configure variables for different environments like development, testing, and production.

## Installation

You can install `envmate` using pip:

```bash
pip install envmate
```

## Usage

After installation, you can use the tool via the command line:

```bash
env-configurator
```

The tool will prompt you to select the Python framework you are using and guide you through setting up the necessary environment variables.

## Example Workflow

```plaintext
$ env-configurator

Welcome to the Python Environment Configuration Tool!

What kind of Python stack are you using?
> Flask
  Django
  FastAPI

Which environment are you configuring?
> development
  testing
  production

Are you building an authentication system? (Y/n): Y

What type of authentication are you using?
> JWT
  Session-based

Do you need access and refresh tokens? (Y/n): Y

Will your application use email protocols? (y/N): N

Will your application use Redis? (y/N): N

Will your application use SQL databases? (Y/n): Y

Will your application use NoSQL databases? (y/N): Y

Will your application use Elasticsearch? (y/N): N

Flask environment:
> development
  production

Flask secret key: <generated_secret>
Enable debug mode? (y/N): Y

CORS origins: http://localhost:3000

Which NoSQL database are you using?
> MongoDB
  Cassandra

MongoDB URI: mongodb://localhost:27017

Configuration Summary:
FLASK_ENV=development
SECRET_KEY=<generated_secret>
DEBUG=True
CORS_ORIGINS=http://localhost:3000
MONGODB_URI=mongodb://localhost:27017

Here is the summary of your configuration. Do you want to write it to the .env file? (Y/n): Y
.env variables have been written successfully.
Do you want to save this configuration as a template? (y/N): N

Process completed successfully!
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for more information on how to contribute to this project.

## Issues

If you encounter any issues or have suggestions for improvements, please report them on the [GitHub issue tracker](https://github.com/yourusername/envmate/issues).

## Author

Developed by [harris-ahmad](https://github.com/harris-ahmad).