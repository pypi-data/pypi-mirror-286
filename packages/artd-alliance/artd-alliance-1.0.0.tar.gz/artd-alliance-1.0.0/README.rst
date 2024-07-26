ArtD Alliance
==============
Art Alliance is a package that makes it possible to manage allies and alliance.
---------------------------------------------------------------------------------------------------
1. Add to your INSTALLED_APPS setting like this:

.. code-block:: python

    INSTALLED_APPS = [
        'artd_module',
        'artd_location',
        'artd_partner',
        'artd_alliance',

    ]

1. Run the migration commands:
   
.. code-block::
    
        python manage.py makemigrations
        python manage.py migrate

3. Run the seeder data:
   
.. code-block::

        python manage.py create_countries
        python manage.py create_colombian_regions
        python manage.py create_colombian_cities

4. Add context processors

.. code-block::

        TEMPLATES = [
            {
                'OPTIONS': {
                    'context_processors': [
                        ...
                        'artd_alliance.context_processors.user_context_processor',
                        ...
                    ],
                },
            },
        ]