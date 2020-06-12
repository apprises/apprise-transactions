## Description:
**Related issue (if applicable):** #<!--apprises issue number goes here-->

<!-- Have anything else to describe? Define it here -->

## New Payment Platform Completion Status
<!-- This section is only applicable if you're adding a new service -->
* [ ] apprisetransactions/factories/<!--paymentplatform goes here-->_factory.py
    - import transaction factory within factories/__init__.py
* [ ] apprisetransactions/transactions/<!--paymentplatform goes here-->_transaction.py
    - import transaction type within transactions/__init__.py
* [ ] apprisetransactions/__init__.py
    - import transaction type / transaction factory and at to the __all__ list
* [ ] apprisetransactions/exceptions/
    - add applicable exceptions to files
* [ ] setup.py
    - add new payment platform into the `keywords` section of the `setup()` declaration
* [ ] README.md
    - add entry for new payment platform to table (as a quick reference)

## Checklist
<!-- The following must be completed or your PR can't be merged -->
* [ ] The code change is tested and works locally.
* [ ] There is no commented out code in this PR.
* [ ] No lint errors (use `flake8`)
* [ ] 100% test coverage
