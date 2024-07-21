
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.




# Created on Jul 27, 2019
#
# @author: ballance

from vsc.model.constraint_model import ConstraintModel
from vsc.model.expr_model import ExprModel


class ConstraintExprModel(ConstraintModel):
    
    def __init__(self, e):
        super().__init__()
        self.e = e
        
    def build(self, btor, soft=False):
        return ExprModel.toBool(btor, self.e.build(btor))
        
    def accept(self, visitor):
        visitor.visit_constraint_expr(self)
        
    def clone(self, deep=False)->'ConstraintModel':
        ret = ConstraintExprModel(self.e)
        
        if deep:
            print("TODO: ")
            
        return ret
        
