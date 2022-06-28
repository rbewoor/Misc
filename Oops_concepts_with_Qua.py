import numpy as np

"""
My notes on methods types and basic OOPs stuff
Classmethod vs Staticmethod:
https://www.geeksforgeeks.org/class-method-vs-static-method-python/

A static method does not receive an implicit first argument. A static
method is also a method that is bound to the class and not the object
of the class. This method cannot access or modify the class state. It
is present in a class because it makes sense for the method to be
present in class.

The difference between the Class method and the static method is:
- A class method takes cls as the first parameter while a static
  method needs no specific parameters.
- A class method can access or modify the class state while a
  static method can’t access or modify it.
- In general, static methods know nothing about the class state.
  They are utility-type methods that take some parameters and work
  upon those parameters. On the other hand class methods must have
  class as a parameter.
- We use @classmethod decorator in python to create a class method and we use
  @staticmethod decorator to create a static method in python.
- We generally use the class method to create factory methods. Factory methods
  return class objects ( similar to a constructor ) for different use cases.
- We generally use static methods to create utility functions.
"""


class Quaternion:
    """
    Quaternion is an extension of complex numbers with 3 imaginary parts.
    This class has various methods to perform basic operations like
    create, add, display, scale, norm, etc.
    """
    # Class variable shared across all objects.
    #   we could change the value for a particular instance but that
    #   is not what we should be doing ideally.
    # Putting __ before the name makes it a hidden variable i.e. the
    #   variable can only be accessed by code within the class.
    # Let if we really still want to access the hidden variable we
    #   can do so as follows:
    #   <<object-name>>._<<class-name>>__<<hidden-variable>>
    #   e.g.: q2._Quaternion__unit_vectors
    __unit_vectors = ['', 'i', 'j', 'k']

    def __init__(self, _a=0, _b=0, _c=0, _d=0):
        """
        Expects upto four numerical values as the coefficients.
        Will convert to float and round to 2 decimals.
        """
        input_values = [_a, _b, _c, _d]
        if not all([isinstance(v, (int, float)) for v in input_values]):
            print(''.join([
                'Error: Cannot create Quaternion (non-numerical',
                ' data) provided.',
            ]))
        else:
            input_values = [round(float(v), 2) for v in input_values]
            self.coeffs = input_values
        return

    def scalar_multiplication(self, scalar):
        try:
            scaled_coeff = list(np.array(self.coeffs) * scalar)
            scaled_coeff = [round(v, 2) for v in scaled_coeff]
            return Quaternion(*scaled_coeff)
        except Exception as e:
            print(
                ''.join([
                    'Problem in method: scalar_multiplication. ',
                    f'Error message: {e}',
                ])
            )

    def real_part(self):
        try:
            return self.coeffs[0]
        except Exception as e:
            raise ValueError(
                ''.join([
                    'Problem in method: real_part. ',
                    f'Error message: {e}',
                ])
            )

    def conjugate(self):
        try:
            conj_coeffs = [self.coeffs[0]] + list(
                map(lambda x: x*-1, self.coeffs[1:])
            )
            return Quaternion(*conj_coeffs)
        except Exception as e:
            raise ValueError(
                ''.join([
                    'Problem in method: conjugate. ',
                    f'Error message: {e}',
                ])
            )

    def norm(self):
        try:
            np_coeffs = np.array(self.coeffs)
            return round(np.sqrt(np.sum(np_coeffs**2)), 2)
        except Exception as e:
            raise ValueError(
                ''.join([
                    'Problem in method: norm. ',
                    f'Error message: {e}',
                ])
            )

    @staticmethod
    def create_real_quarternion(scalar):
        if not isinstance(scalar, (int, float)):
            raise ValueError(''.join([
                'Problem in method: create_real_quarternion.',
                'Cannot create real Quaternion',
                ' (non-numerical data) provided.',
            ]))
        else:
            return Quaternion(_a=scalar)

    @classmethod
    def create_multiple_real_quarternion(cls, scalar_list):
        try:
            return [Quaternion(scalar) for scalar in scalar_list]
        except Exception as e:
            print(''.join([
                'Problem in method: create_multiple_real_quarternion.',
                f'Error message: {e}',
            ]))

    def __str__(self):
        """
        You can change what gets printed by defining a special instance method
        called __str__().
        Here we are going to print the usual way a quaternion is written when
        the print function is called on an object.
        If there is no __str__ method defined, print will simply show the
        address at which the object is created.
        Alternative is to use __repr__. But __str___ takes precedence over
           __repr__ when the print function is invoked.
        """
        try:
            answer = ' '.join([
                f'{coeff:+.2f}{vector}' for coeff, vector
                in zip(self.coeffs, Quaternion.__unit_vectors)
            ])
            # answer = ' '.join([
            #     f'{self.coeffs[0]:+.2f}',
            #     f'{self.coeffs[1]:+.2f}i',
            #     f'{self.coeffs[2]:+.2f}j',
            #     f'{self.coeffs[3]:+.2f}k',
            # ])
            return answer
        except Exception as e:
            raise ValueError(
                ''.join([
                    'Problem in method: __str__. ',
                    f'Error message: {e}',
                ])
            )

    def __add__(self, other_q):
        if not isinstance(other_q, Quaternion):
            print(''.join([
                'Problem in __add__. Other operand is not a',
                f' Quaternion but is of type = {type(other_q)}',
            ]))
        else:
            add_coeffs = list(np.array(self.coeffs) + np.array(other_q.coeffs))
            return Quaternion(*add_coeffs)


class QuaternionHelper:
    """
    Helper class to perform certain actions on a Quarternion.

    Inputs:
        input_quarternion (Quarternion): input Quaternion
        action (str): Type of action to perform.
                      Valid actions are:
                        1) real_part: print the real part of the
                                      input Quaternion
                        2) conjugate: print the conjugate of the
                                      input Quaternion
                        3) norm: print the norm of the input quaternion
                        4) itself: print the input Quaternion
                        5) triple: print the result of multiplication of
                                   the input Quaternion and 3
                        6) other input: throw appropriate error
    Returns:
        Nothing
    """
    @staticmethod
    def perform_on_quarternion(input_quaternion, action):
        if not isinstance(input_quaternion, Quaternion):
            print(
                ''.join([
                    'Error: Input parameter is not a Quaternion,'
                    f' but of type = {type(input_quaternion)}',
                ])
            )
            return
        action_dict = {
            'real_part': lambda q: q.real_part(),
            'conjugate': lambda q: q.conjugate(),
            'norm': lambda q: q.norm(),
            'itself': lambda q: q.__str__(),
            'triple': lambda q: q.scalar_multiplication(3),
        }
        try:
            qh_answer = action_dict[action](input_quaternion)
            print(
                f'qh_answer = {qh_answer}'
            )
        except KeyError:
            print(
                f'Error QuarternionHelper: Invalid action = {action}.'
            )
        return


def do_main():
    print(f'\n{"-"*5} Test: create new quaternion')
    q1 = Quaternion(-6, 8, -8, 6)
    print(f'q1 = {q1}')

    print(f'\n{"-"*5} Test: norm')
    q1_norm = q1.norm()
    print(f'q1_norm = {q1_norm}')

    print(f'\n{"-"*5} Test: addition')
    q2 = Quaternion(-1.46956, -2, 3.21, -4)
    print(f'q1 = {q1}\nq2 = {q2}')
    q3 = q2 + q1
    print(f'q3 = q1 + q2 = {q3}')

    print(f'\n{"-"*5} Test: real part')
    q2_real_part = q2.real_part()
    print(f'q2_real_part = {q2_real_part}')

    print(f'\n{"-"*5} Test: conjugate')
    q2_conj = q2.conjugate()
    print(f'q2_conj = {q2_conj}')

    print(f'\n{"-"*5} Test: scalar multiplication')
    scale_factor = 1.5
    q1_scaled = q1.scalar_multiplication(scale_factor)
    print(f'q1_scaled with {scale_factor} = {q1_scaled}')
    print(f'\n{"-"*5} Test: scalar multiplication (failure)')
    scale_factor = '1.5'
    q1_scaled = q1.scalar_multiplication(scale_factor)
    print(f'q1_scaled with {scale_factor} = {q1_scaled}')

    input_scalar_values = list(range(-14, 8, 7))
    print(f'\n{"-"*5} Test: create one real quaternion')
    q_real_one = Quaternion.create_real_quarternion(input_scalar_values[0])
    print(''.join([
        'Created one real Quaternion with scalar =',
        f' {input_scalar_values[0]} =>> {q_real_one}'
    ]))
    print(f'\n{"-"*5} Test: create multiple real quaternion')
    q_multiple_real = \
        Quaternion.create_multiple_real_quarternion(input_scalar_values)
    for i, each_q in enumerate(q_multiple_real):
        print(''.join([
            f'{i+1}) Real Quaternion with scalar =',
            f' {input_scalar_values[i]}) =>> {each_q}',
            ])
        )

    print(f'\n{"-"*5} QuarternionHelper related... {"-"*5}')
    print(f'Testing using input as q1 = {q1}')
    actions_test = [
        'real_part',
        'conjugate',
        'norm',
        'itself',
        'triple',
        'blah'
    ]
    for an_action in actions_test:
        print(f'{"-"*5} Test Quarternion: action = {an_action}')
        QuaternionHelper.perform_on_quarternion(q1, an_action)

    print(f'{"-"*5} Test Quarternion: invalid object (failure)')
    QuaternionHelper.perform_on_quarternion(123, 'blahblah')

    print(f'\n{"-"*5} Extra OOPs stuff for myself {"-"*5}')
    # accessing hidden variable wrong way
    try:
        print(f'Hidden variable wrong way = {q1.__unit_vectors}')
    except Exception as e:
        print(f'Accessed hidden variable incorrectly. Exception message: {e}')
    # accessing hidden variable correct way
    try:
        print(f'Hidden variable correctly = {q1._Quaternion__unit_vectors}')
    except Exception as e:
        print(f'Accessed hidden variable incorrectly. Exception message: {e}')

    print('\n\nDone\n')
    return


if __name__ == '__main__':
    do_main()
