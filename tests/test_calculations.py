import pytest
from app.calculations import add



# a function that runs before a specific test
@pytest.fixture
def zero_bank_account():

    # return BankAccount(intialize_value=0)
    pass


@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5), 
    (7, 1, 8),
    (12, 4, 16),
    (1, 1, 2),
])


def test_add(num1, num2, expected):
    print ("testing add function")
    assert  add(num1,num2) == expected


# using a fixture
# def test_bank_initial(zero_bank_account):
#     print ("testing add function")
#     assert  bank_account.balance == 0






# def test_add():
#     print ('testing add')
#     sum = add(5, 3)
#     assert sum == 8



# test_add()