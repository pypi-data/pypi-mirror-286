from setuptools import setup, find_packages

setup(name='django_keycloak_lma_cut',
      version='0.1.0',
      description='Cut down version of the package django_keycloak_lma',
      long_description="""
INFO:
\n
settings.KEYCLOAK_OIDC_PROFILE_MODEL = OpenIdConnectProfile

Available features:
- bearer token auth with introspect and user creation (KeycloakTokenAuthentication)
- permission check (auth/permissions)
\n
Examples of using features: tests/lma
""",
      long_description_content_type='text/markdown',
      author='Vyacheslav Konovalov',
      packages=find_packages(),
      install_requires=[
            'djangorestframework',
            'python-keycloak-client-pkg',
      ],
      include_package_data=True,
      zip_safe=False)
