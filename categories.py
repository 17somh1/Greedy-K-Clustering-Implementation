import pandas as pd

# categories = ['workclass', 'marital', 'occupation', 'race', 'sex', 'native_country']
categories = ['workclass','sex', 'native_country']
# Add a new global variable for numeric attributes
# numeric_attributes = ['age', 'education_num']
numeric_attributes = ['education_num']


def load_data(data_file):
    # Load the dataset
    data = pd.read_csv(data_file)

    # Replace missing values, assuming '?' represents missing data
    data = data.replace('?', pd.NA)

    # Drop rows with missing values
    data = data.dropna()

    # Convert categorical attributes to the 'category' data type
    for attr in categories:
        data[attr] = data[attr].astype('category')

    # Reset the index after dropping rows
    data = data.reset_index(drop=True)

    return data, numeric_attributes, categories


marital_status_tree = {
    'value': 'root',
    'children': [
        {
            'value': 'Married',
            'children': [
                {
                    'value': 'Married-civ-spouse',
                    'children': []
                },
                {
                    'value': 'Married-spouse-absent',
                    'children': []
                },
                {
                    'value': 'Married-AF-spouse',
                    'children': []
                }
            ]
        },
        {
            'value': 'Unmarried',
            'children': [
                {
                    'value': 'Never-married',
                    'children': []
                },
                {
                    'value': 'Divorced',
                    'children': []
                },
                {
                    'value': 'Separated',
                    'children': []
                },
                {
                    'value': 'Widowed',
                    'children': []
                }
            ]
        },
    ]
}
occupation_tree = {
    'value': 'root',
    'children': [
        {
            'value': 'Management and Professional',
            'children': [
                {
                    'value': 'Management',
                    'children': [
                        {
                            'value': 'Executive Management',
                            'children': [
                                {
                                    'value': 'Exec-managerial',
                                    'children': []
                                }
                            ]
                        }
                    ]
                },
                {
                    'value': 'Professional',
                    'children': [
                        {
                            'value': 'Specialty Professions',
                            'children': [
                                {
                                    'value': 'Prof-specialty',
                                    'children': []
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            'value': 'Technical, Trade, and Labor',
            'children': [
                {
                    'value': 'Technical and Trade',
                    'children': [
                        {
                            'value': 'Technical Support',
                            'children': [
                                {
                                    'value': 'Tech-support',
                                    'children': []
                                }
                            ]
                        },
                        {
                            'value': 'Craft and Repair',
                            'children': [
                                {
                                    'value': 'Craft-repair',
                                    'children': []
                                }
                            ]
                        },
                        {
                            'value': 'Machine Operation and Inspection',
                            'children': [
                                {
                                    'value': 'Machine-op-inspct',
                                    'children': []
                                }
                            ]
                        }
                    ]
                },
                {
                    'value': 'Labor',
                    'children': [
                        {
                            'value': 'Transport and Moving',
                            'children': [
                                {
                                    'value': 'Transport-moving',
                                    'children': []
                                }
                            ]
                        },
                        {
                            'value': 'Farming and Fishing',
                            'children': [
                                {
                                    'value': 'Farming-fishing',
                                    'children': []
                                }
                            ]
                        },
                        {
                            'value': 'Handlers and Cleaners',
                            'children': [
                                {
                                    'value': 'Handlers-cleaners',
                                    'children': []
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            'value': 'Sales, Marketing, and Service',
            'children': [
                {
                    'value': 'Sales and Marketing',
                    'children': [
                        {
                            'value': 'Sales',
                            'children': []
                        }
                    ]
                },
                {
                    'value': 'Service',
                    'children': [
                        {
                            'value': 'Other Services',
                            'children': [
                                {
                                    'value': 'Other-service',
                                    'children': []
                                }
                            ]
                        },
                        {
                            'value': 'Protective Services',
                            'children': [
                                {
                                    'value': 'Protective-serv',
                                    'children': []
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            'value': 'Clerical, Administrative, and Domestic',
            'children': [
                {
                    'value': 'Clerical and Administrative',
                    'children': [
                        {
                            'value': 'Administrative and Clerical',
                            'children': [
                                {
                                    'value': 'Adm-clerical',
                                    'children': []
                                }
                            ]
                        }
                    ]
                },
                {
                    'value': 'Domestic Services',
                    'children': [
                        {
                            'value': 'Private Household Services',
                            'children': [
                                {
                                    'value': 'Priv-house-serv',
                                    'children': []
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            'value': 'Military',
            'children': [
                {
                    'value': 'Armed Forces',
                    'children': [
                        {
                            'value': 'Armed-Forces',
                            'children': []
                        }
                    ]
                }
            ]
        }
    ]
}



relationship_tree = {
    'value': 'root',
    'children': [
        {
            'value': 'Husband',
            'children': []
        },
        {
            'value': 'Wife',
            'children': []
        },
        {
            'value': 'Child',
            'children': []
        },
        {
            'value': 'Not-in-family',
            'children': []
        },
        {
            'value': 'Other-relative',
            'children': []
        },
        {
            'value': 'Unmarried',
            'children': []
        }
    ]
}

race_tree = {
    'value': 'root',
    'children': [
        {
            'value': 'White',
            'children': []
        },
        {
            'value': 'Black',
            'children': []
        },
        {
            'value': 'Asian-Pac-Islander',
            'children': []
        },
        {
            'value': 'Amer-Indian-Eskimo',
            'children': []
        },
        {
            'value': 'Other',
            'children': []
        }
    ]
}

sex_tree = {
    'value': 'root',
    'children': [
        {
            'value': 'Male',
            'children': []
        },
        {
            'value': 'Female',
            'children': []
        }
    ]
}

workclass_tree = {
    'value': 'root',
    'children': [
        {
            'value': 'Employed',
            'children': [
                {
                    'value': 'Private',
                    'children': []
                },
                {
                    'value': 'Self-emp',
                    'children': [
                        {
                            'value': 'Self-emp-not-inc',
                            'children': []
                        },
                        {
                            'value': 'Self-emp-inc',
                            'children': []
                        }
                    ]
                },
                {
                    'value': 'Government',
                    'children': [
                        {
                            'value': 'Federal-gov',
                            'children': []
                        },
                        {
                            'value': 'State-gov',
                            'children': []
                        },
                        {
                            'value': 'Local-gov',
                            'children': []
                        }
                    ]
                }
            ]
        },
        {
            'value': 'Unpaid',
            'children': [
                {
                    'value': 'Without-pay',
                    'children': []
                },
                {
                    'value': 'Never-worked',
                    'children': []
                }
            ]
        }
    ]
}

native_country_tree = {
    'value': 'root',
    'children': [
        {
            'value': 'America',
            'children': [
                {
                    'value': 'North America',
                    'children': [
                        {
                            'value': 'United-States',
                            'children': []
                        },
                        {
                            'value': 'Canada',
                            'children': []
                        },
                        {
                            'value': 'Mexico',
                            'children': []
                        },
                    ]
                },
                {
                    'value': 'South America',
                    'children': [
                        {
                            'value': 'Columbia',
                            'children': []
                        },
                        {
                            'value': 'Ecuador',
                            'children': []
                        },
                        {
                            'value': 'Peru',
                            'children': []
                        },
                    ]
                },
                {
                    'value': 'Central America',
                    'children': [
                        {
                            'value': 'Honduras',
                            'children': []
                        },
                        {
                            'value': 'Guatemala',
                            'children': []
                        },
                        {
                            'value': 'Nicaragua',
                            'children': []
                        },
                        {
                            'value': 'El-Salvador',
                            'children': []
                        },
                    ]
                },
                {
                    'value': 'Caribbean',
                    'children': [
                        {
                            'value': 'Cuba',
                            'children': []
                        },
                        {
                            'value': 'Jamaica',
                            'children': []
                        },
                        {
                            'value': 'Haiti',
                            'children': []
                        },
                        {
                            'value': 'Dominican-Republic',
                            'children': []
                        },
                        {
                            'value': 'Trinadad&Tobago',
                            'children': []
                        },
                        {
                            'value': 'Puerto-Rico',
                            'children': []
                        },
                    ]
                },
            ]
        },
        {
            'value': 'Eurasia',
            'children': [{
                'value': 'Asia',
                'children': [
                    {
                        'value': 'India',
                        'children': []
                    },
                    {
                        'value': 'China',
                        'children': []
                    },
                    {
                        'value': 'Japan',
                        'children': []
                    },
                    {
                        'value': 'Vietnam',
                        'children': []
                    },
                    {
                        'value': 'Taiwan',
                        'children': []
                    },
                    {
                        'value': 'Iran',
                        'children': []
                    },
                    {
                        'value': 'Philippines',
                        'children': []
                    },
                    {
                        'value': 'Cambodia',
                        'children': []
                    },
                    {
                        'value': 'Laos',
                        'children': []
                    },
                    {
                        'value': 'Thailand',
                        'children': []
                    },
                    {
                        'value': 'Hong',
                        'children': []
                    },
                ]
            },
                {
                    'value': 'Europe',
                    'children': [
                        {
                            'value': 'England',
                            'children': []
                        },
                        {
                            'value': 'Germany',
                            'children': []
                        },
                        {
                            'value': 'Italy',
                            'children': []
                        },
                        {
                            'value': 'Poland',
                            'children': []
                        },
                        {
                            'value': 'Portugal',
                            'children': []
                        },
                        {
                            'value': 'Greece',
                            'children': []
                        },
                        {
                            'value': 'France',
                            'children': []
                        },
                        {
                            'value': 'Ireland',
                            'children': []
                        },
                        {
                            'value': 'Scotland',
                            'children': []
                        },
                        {
                            'value': 'Yugoslavia',
                            'children': []
                        },
                        {
                            'value': 'Hungary',
                            'children': []
                        },
                        {
                            'value': 'Holand-Netherlands',
                            'children': []
                        },
                    ]
                },

            ]
        },
        {
            'value': 'Oceania',
            'children': [
                {
                    'value': 'Outlying-US(Guam-USVI-etc)',
                    'children': []
                },
                {
                    'value': 'New Zealand',
                    'children': []
                },
                {
                    'value': 'Australia',
                    'children': []
                },
            ]
        },
    ]
}

education_tree = {
    'value': 'root',
    'children': [
        {
            'value': 'No degree',
            'children': [
                {
                    'value': 'Preschool',
                    'children': []
                },
                {
                    'value': 'Primary',
                    'children': [
                        {
                            'value': '1st-4th',
                            'children': []
                        },
                        {
                            'value': '5th-6th',
                            'children': []
                        }
                    ]
                },
                {
                    'value': 'Secondary',
                    'children': [
                        {
                            'value': '7th-8th',
                            'children': []
                        },
                        {
                            'value': '9th',
                            'children': []
                        },
                        {
                            'value': '10th',
                            'children': []
                        },
                        {
                            'value': '11th',
                            'children': []
                        },
                        {
                            'value': '12th',
                            'children': []
                        },
                        {
                            'value': 'HS-grad',
                            'children': []
                        }
                    ]
                },
            ]
        },
        {
            'value': 'Some-college',
            'children': [
                {
                    'value': 'Associate degree',
                    'children': [
                        {
                            'value': 'Assoc-acdm',
                            'children': []
                        },
                        {
                            'value': 'Assoc-voc',
                            'children': []
                        }
                    ]
                },
                {
                    'value': 'Bachelor degree',
                    'children': [
                        {
                            'value': 'Bachelors',
                            'children': []
                        }
                    ]
                },
                {
                    'value': 'Postgraduate degree',
                    'children': [
                        {
                            'value': 'Masters',
                            'children': []
                        },
                        {
                            'value': 'Doctorate',
                            'children': []
                        },
                        {
                            'value': 'Prof-school',
                            'children': []
                        }
                    ]
                }
            ]
        },
    ]
}

taxonomy_trees = [
    {
        'attribute': 'workclass',
        'tree': workclass_tree
    },
    {
        'attribute': 'education',
        'tree': education_tree
    },
    {
        'attribute': 'marital',
        'tree': marital_status_tree
    },
    {
        'attribute': 'occupation',
        'tree': occupation_tree
    },
    {
        'attribute': 'relationship',
        'tree': relationship_tree
    },
    {
        'attribute': 'race',
        'tree': race_tree
    },
    {
        'attribute': 'sex',
        'tree': sex_tree
    },
    {
        'attribute': 'native_country',
        'tree': native_country_tree
    }
]
