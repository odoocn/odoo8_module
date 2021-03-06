# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.tests import common
from openerp import exceptions


class TestModelCause(common.TransactionCase):

    def test_create_cause(self):
        record = self.env['mgmtsystem.nonconformity.cause'].create({
            "name": "TestCause",
        })

        self.assertNotEqual(record.id, 0)
        self.assertNotEqual(record.id, None)

    def test_name_get(self):

        record = self.env['mgmtsystem.nonconformity.cause'].create({
            "name": "TestCause",
        })

        name_assoc = record.name_get()

        self.assertEqual(name_assoc[0][1], "TestCause")
        self.assertEqual(name_assoc[0][0], record.id)

        record2 = self.env['mgmtsystem.nonconformity.cause'].create({
            "name": "test2",
            "parent_id": record.id
        })

        name_assoc = record2.name_get()

        self.assertEqual(name_assoc[0][1], "TestCause / test2")
        self.assertEqual(name_assoc[0][0], record2.id)

        record3 = self.env['mgmtsystem.nonconformity.cause'].create({
            "name": "test3",
            "parent_id": record2.id
        })

        name_assoc = record3.name_get()

        self.assertEqual(name_assoc[0][1], "TestCause / test2 / test3")
        self.assertEqual(name_assoc[0][0], record3.id)

    def test_recursion(self):
        parent = self.env['mgmtsystem.nonconformity.cause'].create({
            "name": "ParentCause",
        })
        child = self.env['mgmtsystem.nonconformity.cause'].create({
            "name": "ChildCause",
            "parent_id": parent.id,
        })
        with self.assertRaises(exceptions.ValidationError):
            parent.write({"parent_id": child.id})
