/*!
 * Isomer - The distributed application framework
 * ==============================================
 * Copyright (C) 2011-2019 Heiko 'riot' Weinen <riot@c-base.org> and others.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

'use strict';

//import SocialCalc from 'socialcalc';

/**
 * @ngdoc function
 * @name isomerFrontendApp.controller:CalcCtrl
 * @description
 * # CalcCtrl
 * Controller of the isomerFrontendApp
 */
class CalcCtrl {
    constructor($scope, $rootScope, $compile, ObjectProxy, moment, notification, socket, user) {
        this.scope = $scope;
        this.rootscope = $rootScope;
        this.compile = $compile;
        this.moment = moment;
        this.op = ObjectProxy;
        this.notification = notification;
        this.socket = socket;
        this.user = user;

        let self = this;

        if (socket.protocol === 'wss') {
            this.protocol = 'https';
        } else {
            this.protocol = 'http';
        }

        this.hostname = this.protocol + '://' + socket.host;

        if ((this.protocol === 'https' && socket.port !== 443) || (this.protocol === 'http' && socket.port !== 80)) {
            this.hostname += ':' + socket.port;
        }

        this.hostname += '/ethercalc/';
        this.sheetname = 'INITIAL';

        this.sheet = {
            'name': 'Initial',
            'notes': 'Select a sheet to the right!'
        };

        this.sheets = {};

        this.request_sheets = function () {
            console.log('[CALC] Getting sheets');
            self.op.search('spreadsheet', '*', '*').then(function (msg) {
                let sheets = msg.data.list;
                for (let sheet of sheets) {
                    self.sheets[sheet.uuid] = sheet;
                }

                console.log('[CALC] Sheets:', self.sheets);
            })
        };


        this.iframe_url = this.hostname + this.sheetname;

        this.rootscope.$on('User.Login', function () {
            self.request_sheets();
        });

        if (this.user.signedin) {
            this.request_sheets();
        }
    }

    select_sheet() {
        console.log('[CALC] Switching sheet to ', this.sheetname, this.sheets[this.sheetname]);
        this.iframe_url = this.hostname + this.sheetname;
        this.sheet = this.sheets[this.sheetname];
        console.log('[CALC] Sheet:', this.sheet);
    }
}

CalcCtrl.$inject = ['$scope', '$rootScope', '$compile', 'objectproxy', 'moment', 'notification', 'socket', 'user'];

export default CalcCtrl;
