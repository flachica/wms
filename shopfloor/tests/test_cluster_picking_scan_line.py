# Copyright 2020 Camptocamp SA (http://www.camptocamp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from .test_cluster_picking_base import ClusterPickingLineCommonCase


class ClusterPickingScanLineCase(ClusterPickingLineCommonCase):
    """Tests covering the /scan_line endpoint

    After a batch has been selected and the user confirmed they are
    working on it.

    User scans something and the scan_line endpoints validates they
    scanned the proper thing to pick.
    """

    def _scan_line_ok(self, line, scanned):
        batch = line.picking_id.batch_id
        response = self.service.dispatch(
            "scan_line",
            params={
                "picking_batch_id": batch.id,
                "move_line_id": line.id,
                "barcode": scanned,
            },
        )
        self.assert_response(
            response, next_state="scan_destination", data=self._line_data(line)
        )

    def _scan_line_error(self, line, scanned, message):
        batch = line.picking_id.batch_id
        response = self.service.dispatch(
            "scan_line",
            params={
                "picking_batch_id": batch.id,
                "move_line_id": line.id,
                "barcode": scanned,
            },
        )
        self.assert_response(
            response,
            next_state="start_line",
            data=self._line_data(line),
            message=message,
        )

    def test_scan_line_pack_ok(self):
        """Scan to check if user picks the correct pack for current line"""
        self._simulate_batch_selected(self.batch, in_package=True)
        line = self.batch.picking_ids.move_line_ids
        self._scan_line_ok(line, line.package_id.name)

    def test_scan_line_product_ok(self):
        """Scan to check if user picks the correct product for current line"""
        self._simulate_batch_selected(self.batch)
        line = self.batch.picking_ids.move_line_ids
        self._scan_line_ok(line, line.product_id.barcode)

    def test_scan_line_lot_ok(self):
        """Scan to check if user picks the correct lot for current line"""
        self.product_a.tracking = "lot"
        self._simulate_batch_selected(self.batch, in_lot=True)
        line = self.batch.picking_ids.move_line_ids
        self._scan_line_ok(line, line.lot_id.name)

    def test_scan_line_serial_ok(self):
        """Scan to check if user picks the correct serial for current line"""
        self.product_a.tracking = "serial"
        self._simulate_batch_selected(self.batch, in_lot=True)
        line = self.batch.picking_ids.move_line_ids
        self._scan_line_ok(line, line.lot_id.name)

    def test_scan_line_error_product_tracked(self):
        """Scan a product tracked by lot, must scan the lot"""
        self.product_a.tracking = "lot"
        self._simulate_batch_selected(self.batch, in_lot=True)
        line = self.batch.picking_ids.move_line_ids
        self._scan_line_error(
            line,
            line.product_id.barcode,
            {
                "message_type": "warning",
                "body": "Product tracked by lot, please scan one.",
            },
        )

    def test_scan_line_product_error_several_packages(self):
        """When we scan a product which is in more than one package, error"""
        self._simulate_batch_selected(self.batch, in_package=True)
        line = self.batch.picking_ids.move_line_ids
        # create a second move line for the same product in a different
        # package
        move = line.move_id.copy()
        self._fill_stock_for_moves(move, in_package=True)
        move._action_confirm(merge=False)
        move._action_assign()

        self._scan_line_error(
            line,
            move.product_id.barcode,
            {
                "message_type": "warning",
                "body": "This product is part of multiple"
                " packages, please scan a package.",
            },
        )

    def test_scan_line_product_error_in_one_package_and_raw_same_location(self):
        """Scan product which is both in a package and as raw in same location"""
        self._simulate_batch_selected(self.batch, in_package=True)
        line = self.batch.picking_ids.move_line_ids
        # create a second move line for the same product in a different
        # package
        move = line.move_id.copy()
        self._fill_stock_for_moves(move)
        move._action_confirm(merge=False)
        move._action_assign()
        move.move_line_ids[0].package_id = None

        self._scan_line_error(
            line,
            move.product_id.barcode,
            {
                "message_type": "warning",
                "body": "This product is part of multiple"
                " packages, please scan a package.",
            },
        )

    def test_scan_line_product_error_in_one_package_and_raw_different_location(self):
        """Scan product which is both in a package and as raw in another location"""
        self._simulate_batch_selected(self.batch, in_package=True)
        line = self.batch.picking_ids.move_line_ids
        # create a second move line for the same product in a different
        # package
        move = line.move_id.copy()
        self._fill_stock_for_moves(move)
        move._action_confirm(merge=False)
        move._action_assign()
        move.move_line_ids[0].package_id = None
        move.move_line_ids[0].location_id = line.location_id.copy()
        self._scan_line_ok(line, move.product_id.barcode)

    def test_scan_line_lot_error_several_packages(self):
        """When we scan a lot which is in more than one package, error"""
        self._simulate_batch_selected(self.batch, in_package=True, in_lot=True)
        line = self.batch.picking_ids.move_line_ids
        # create a second move line for the same product in a different
        # package
        move = line.move_id.copy()
        self._fill_stock_for_moves(move, in_lot=line.lot_id)
        move._action_confirm(merge=False)
        move._action_assign()

        self._scan_line_error(
            line,
            line.lot_id.name,
            {
                "message_type": "warning",
                "body": "This lot is part of multiple"
                " packages, please scan a package.",
            },
        )

    def test_scan_line_lot_error_in_one_package_and_unit(self):
        """When we scan a lot which is in a package and as raw, error"""
        self._simulate_batch_selected(self.batch, in_package=True, in_lot=True)
        line = self.batch.picking_ids.move_line_ids
        # create a second move line for the same product in a different
        # package
        move = line.move_id.copy()
        self._fill_stock_for_moves(move, in_lot=line.lot_id)
        move._action_confirm(merge=False)
        move._action_assign()
        self._scan_line_error(
            line,
            line.lot_id.name,
            {
                "message_type": "warning",
                "body": "This lot is part of multiple"
                " packages, please scan a package.",
            },
        )

    def test_scan_line_location_ok_single_package(self):
        """Scan to check if user scans a correct location for current line

        If there is only one single package in the location, there is no
        ambiguity so we can use it.
        """
        self._simulate_batch_selected(self.batch, in_package=True)
        line = self.batch.picking_ids.move_line_ids
        self._scan_line_ok(line, line.location_id.barcode)

    def test_scan_line_location_ok_single_product(self):
        """Scan to check if user scans a correct location for current line

        If there is only one single product in the location, there is no
        ambiguity so we can use it.
        """
        self._simulate_batch_selected(self.batch)
        line = self.batch.picking_ids.move_line_ids
        self._scan_line_ok(line, line.location_id.barcode)

    def test_scan_line_location_ok_single_lot(self):
        """Scan to check if user scans a correct location for current line

        If there is only one single lot in the location, there is no
        ambiguity so we can use it.
        """
        self._simulate_batch_selected(self.batch, in_lot=True)
        line = self.batch.picking_ids.move_line_ids
        self._scan_line_ok(line, line.location_id.barcode)

    def test_scan_line_location_error_several_package(self):
        """Scan to check if user scans a correct location for current line

        If there are several packages in the location, user has to scan one.
        """
        self._simulate_batch_selected(self.batch, in_package=True)
        line = self.batch.picking_ids.move_line_ids
        location = line.location_id
        # add a second package in the location
        new_move = line.move_id.copy()
        self._fill_stock_for_moves(new_move, in_package=True, same_package=False)
        new_move._action_confirm(merge=False)
        new_move._action_assign()
        loc_lines = self.env["stock.move.line"].search(
            [
                ("picking_id.picking_type_id", "=", self.picking_type.id),
                ("location_id", "=", location.id),
            ]
        )
        # Ensure lines have different packages and no qty done
        self.assertEqual(len(loc_lines), 2)
        self.assertEqual(len(loc_lines.mapped("package_id")), 2)
        self.assertEqual(loc_lines.mapped("qty_done"), [0.0, 0.0])
        # All lines have to be processed,
        # we cannot go further without scanning a specific package
        self._scan_line_error(
            line,
            location.barcode,
            {
                "message_type": "warning",
                "body": "Several packages found in Stock, please scan a package.",
            },
        )
        # Although, if one line is already processed,
        # we can work automatically on the next one
        line.qty_done = line.product_uom_qty
        self._scan_line_ok(new_move.move_line_ids[0], line.location_id.barcode)

    def test_scan_line_location_error_several_products(self):
        """Scan to check if user scans a correct location for current line

        If there are several products in the location, user has to scan one.
        """
        self._simulate_batch_selected(self.batch)
        line = self.batch.picking_ids.move_line_ids
        location = line.location_id
        # add a second product in the location
        self._update_qty_in_location(location, self.product_b, 10)
        # add a second product in the location
        new_move = line.move_id.copy({"product_id": self.product_c.id})
        self._fill_stock_for_moves(new_move)
        new_move._action_confirm(merge=False)
        new_move._action_assign()
        loc_lines = self.env["stock.move.line"].search(
            [
                ("picking_id.picking_type_id", "=", self.picking_type.id),
                ("location_id", "=", location.id),
            ]
        )
        # Ensure lines have no package, 2 products and no qty done
        self.assertEqual(len(loc_lines), 2)
        self.assertEqual(len(loc_lines.mapped("package_id")), 0)
        self.assertEqual(len(loc_lines.mapped("product_id")), 2)
        self.assertEqual(loc_lines.mapped("qty_done"), [0.0, 0.0])
        self._scan_line_error(
            line,
            location.barcode,
            {
                "message_type": "warning",
                "body": "Several products found in Stock, please scan a product.",
            },
        )
        # Although, if one line is already processed,
        # we can work automatically on the next one
        line.qty_done = line.product_uom_qty
        self._scan_line_ok(new_move.move_line_ids[0], line.location_id.barcode)

    def test_scan_line_location_error_several_lots(self):
        """Scan to check if user scans a correct location for current line

        If there are several lots in the location, user has to scan one.
        """
        self._simulate_batch_selected(self.batch, in_lot=True)
        line = self.batch.picking_ids.move_line_ids
        location = line.location_id
        # add a second lot in the location
        new_move = line.move_id.copy()
        self._fill_stock_for_moves(new_move, in_lot=True)
        new_move._action_confirm(merge=False)
        new_move._action_assign()
        loc_lines = self.env["stock.move.line"].search(
            [
                ("picking_id.picking_type_id", "=", self.picking_type.id),
                ("location_id", "=", location.id),
            ]
        )
        # Ensure lines have no package, 1 product, 2 lots and no qty done
        self.assertEqual(len(loc_lines), 2)
        self.assertEqual(len(loc_lines.mapped("package_id")), 0)
        self.assertEqual(len(loc_lines.mapped("product_id")), 1)
        self.assertEqual(len(loc_lines.mapped("lot_id")), 2)
        self.assertEqual(loc_lines.mapped("qty_done"), [0.0, 0.0])
        self._scan_line_error(
            line,
            location.barcode,
            {
                "message_type": "warning",
                "body": "Several lots found in Stock, please scan a lot.",
            },
        )
        # Although, if one line is already processed,
        # we can work automatically on the next one
        line.qty_done = line.product_uom_qty
        self._scan_line_ok(new_move.move_line_ids[0], line.location_id.barcode)

    def test_scan_line_error_wrong_package(self):
        """Wrong package scanned"""
        self._simulate_batch_selected(self.batch, in_package=True)
        pack = self.env["stock.quant.package"].sudo().create({})
        self._scan_line_error(
            self.batch.picking_ids.move_line_ids,
            pack.name,
            {"message_type": "error", "body": "Wrong pack."},
        )

    def test_scan_line_error_wrong_product(self):
        """Wrong product scanned"""
        self._simulate_batch_selected(self.batch, in_package=True)
        product = (
            self.env["product.product"]
            .sudo()
            .create(
                {
                    "name": "Wrong",
                    "barcode": "WRONGPRODUCT",
                }
            )
        )
        self._scan_line_error(
            self.batch.picking_ids.move_line_ids,
            product.barcode,
            {"message_type": "error", "body": "Wrong product."},
        )

    def test_scan_line_error_wrong_lot(self):
        """Wrong product scanned"""
        self._simulate_batch_selected(self.batch, in_package=True)
        lot = (
            self.env["stock.production.lot"]
            .sudo()
            .create(
                {
                    "name": "WRONGLOT",
                    "product_id": self.batch.picking_ids.move_line_ids[0].product_id.id,
                    "company_id": self.env.company.id,
                }
            )
        )
        self._scan_line_error(
            self.batch.picking_ids.move_line_ids,
            lot.name,
            {"message_type": "error", "body": "Wrong lot."},
        )

    def test_scan_line_error_wrong_location(self):
        """Wrong product scanned"""
        self._simulate_batch_selected(self.batch, in_package=True)
        location = (
            self.env["stock.location"]
            .sudo()
            .create(
                {
                    "name": "Wrong",
                    "barcode": "WRONGLOCATION",
                }
            )
        )
        self._scan_line_error(
            self.batch.picking_ids.move_line_ids,
            location.barcode,
            {"message_type": "error", "body": "Wrong location."},
        )

    def test_scan_line_error_not_found(self):
        """Nothing found for the barcode"""
        self._simulate_batch_selected(self.batch, in_package=True)
        self._scan_line_error(
            self.batch.picking_ids.move_line_ids,
            "NO_EXISTING_BARCODE",
            {"message_type": "error", "body": "Barcode not found"},
        )
