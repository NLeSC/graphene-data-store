from models import Department as DepartmentModel
from models import User as UserModel
from models import Role as RoleModel
from models import Dataset as DatasetModel

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

import pandas as pd
import numpy as np

class Department(SQLAlchemyObjectType):
    class Meta:
        model = DepartmentModel
        interfaces = (relay.Node, )


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node, )


class Role(SQLAlchemyObjectType):
    class Meta:
        model = RoleModel
        interfaces = (relay.Node, )


class JSONScalar(graphene.Scalar):
    """
    Arbitrary JSON Properties for features
    https://github.com/graphql-python/graphene/issues/904
    """

    @staticmethod
    def serialize(value):
        return value

    @staticmethod
    def parse_literal(node):
        return node.value

    @staticmethod
    def parse_value(value):
        return value


class DataCell(graphene.ObjectType):
    column_types = graphene.List(graphene.String)
    column_names = graphene.List(graphene.String)
    columns = graphene.List(JSONScalar)    

    @staticmethod
    def resolve_column_types(self, info):
        return [type(d[0]).__name__ for d in self.raw.values()]

    @staticmethod
    def resolve_column_names(self, info):
        return self.raw

    @staticmethod
    def resolve_columns(self, info):
        # print(self.key_types)        
        return self.raw.values()


class HistCell(graphene.ObjectType):
    freq = graphene.List(graphene.List(graphene.Int))
    bins = graphene.List(JSONScalar)  

    @staticmethod
    def resolve_bins(self, info):
        print('resolve_bins:')
        print('\n')
        # print(self.raw)
        nBins = 3        
        df = pd.DataFrame.from_dict (self.raw)
        print (repr(df.info()))
        # print (repr(df))    
        print(pd.cut(df.x, nBins))
        groups = df.groupby(pd.cut(df.x, nBins))
        print(repr(groups.mean()))
        # print(groups.mean().z)   

        # return df.values.tolist()
        return groups.mean().values.tolist()

    @staticmethod
    def resolve_freq(self, info):
        print('resolve_freq:')
        print('\n')
        nBins = 3
        df = pd.DataFrame.from_dict (self.raw)
        print(pd.cut(df.x, nBins))
        groups = df.groupby(pd.cut(df.x, nBins))
        print(repr(groups.count()))
        return groups.count().values.tolist()


class Dataset(SQLAlchemyObjectType):
    # Return a list of section objects
    data = graphene.Field(DataCell)
    histograms = graphene.Field(HistCell)    

    class Meta:
        model = DatasetModel
        interfaces = (relay.Node, )
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith']
        }

    @staticmethod
    def resolve_data(parent, info):
        # if dataset_name:
        #     print(parent)       
        return parent

    @staticmethod
    def resolve_histograms(parent, info):
        # if dataset_name:
        #     print(parent)
        # print(parent)
        return parent

class Query(graphene.ObjectType):
    node = relay.Node.Field()

    # Allow only single column sorting
    all_users = SQLAlchemyConnectionField(
        User, sort=User.sort_argument())

    # Allows sorting over multiple columns, by default over the primary key
    all_roles = SQLAlchemyConnectionField(Role)

    # Disable sorting over this field
    all_departments = SQLAlchemyConnectionField(Department, sort=None)

    # Disable sorting over this field
    all_datasets = SQLAlchemyConnectionField(Dataset)

    dataset = relay.Node.Field(Dataset)

    # dataset_by_name = SQLAlchemyConnectionField(Dataset, name=graphene.String(required=True))
    # def resolve_dataset_by_name(parent, info, name):
    #     return get_dataset(name=name)

    # dataset = SQLAlchemyConnectionField(Dataset, id=graphene.ID(required=True))
    # def resolve_dataset(root, info, id):
    #    return get_dataset_by_id(id)

    # find_dataset = SQLAlchemyConnectionField(Dataset, name = graphene.String())
    # def resolve_find_dataset(self, info, name):
    #   query = Dataset.get_query(info)
    #   print(query)
    #   return query.filter(Dataset.name == name).first()




schema = graphene.Schema(query=Query, types=[Department, User, Role, Dataset])
