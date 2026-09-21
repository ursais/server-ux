/* @odoo-module */

import { Component, usePlugin } from "@odoo/owl";
import {registry} from "@web/core/registry";
import { ActionManagerPlugin } from "@web/webclient/actions/action_plugin";

export class DocumentQuickAccessSystrayItem extends Component {
    static template = "document_quick_access_launcher.view.Menu";
    setup() {
        this.action = usePlugin(ActionManagerPlugin);
    }
    onClick(ev) {
        ev.preventDefault();
        ev.stopPropagation();
        var context = {};
        context.default_model = "document.quick.access.rule";
        context.default_method = "read_code_action";
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Search QR",
            res_model: "barcode.action",
            views: [[false, "form"]],
            target: "new",
            context: context,
        });
    }
}
registry
    .category("systray")
    .add("document_quick_access_launcher", {Component: DocumentQuickAccessSystrayItem});
