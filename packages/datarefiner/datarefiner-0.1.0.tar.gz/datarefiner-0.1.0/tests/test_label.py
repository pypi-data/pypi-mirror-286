#!/usr/bin/env python
# Created by "Thieu" at 21:55, 25/07/2024 ----------%                                                                               
#       Email: nguyenthieu2102@gmail.com            %                                                    
#       Github: https://github.com/thieu1995        %                         
# --------------------------------------------------%

import pytest
from datarefiner import LabelEncoder


@pytest.fixture
def label_encoder():
    data = ['cat', 'dog', 'cat', 'fish', 'dog']
    le = LabelEncoder()
    le.fit(data)
    return le


def test_label_encoder_transform(label_encoder):
    data = ['cat', 'dog', 'cat', 'fish', 'dog']
    encoded_data = label_encoder.transform(data)
    assert list(encoded_data) == [0, 1, 0, 2, 1]


def test_label_encoder_inverse_transform(label_encoder):
    encoded_data = [0, 1, 0, 2, 1]
    decoded_data = label_encoder.inverse_transform(encoded_data)
    assert list(decoded_data) == ['cat', 'dog', 'cat', 'fish', 'dog']


def test_label_encoder_classes(label_encoder):
    classes = label_encoder.unique_labels
    assert list(classes) == ['cat', 'dog', 'fish']


if __name__ == "__main__":
    pytest.main()
