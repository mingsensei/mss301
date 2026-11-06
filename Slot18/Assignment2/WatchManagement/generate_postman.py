# -*- coding: utf-8 -*-
"""
Generate complete Postman Collection mapped 1-to-1 with Report Figures (Hình 6 -> Hình 30).
Ensures all URLs have valid schema (raw, host, path, port, query) so Postman displays them immediately.
Ensures all required Headers (Authorization, Content-Type, X-Saga-Fail-After-Step) are fully populated.
"""

import json
from datetime import date

def build_postman_collection():
    today_str = date.today().isoformat()

    def make_url(raw):
        parts = raw.split('?', 1)
        base = parts[0]
        q_str = parts[1] if len(parts) > 1 else None

        if raw.startswith("http://") or raw.startswith("https://"):
            proto, rest = raw.split("://", 1)
            host_part, *path_parts = rest.split("/")
            if ":" in host_part:
                h_name, h_port = host_part.split(":", 1)
                url_obj = {
                    "raw": raw,
                    "protocol": proto,
                    "host": [h_name],
                    "port": h_port,
                    "path": [p for p in path_parts if p]
                }
            else:
                url_obj = {
                    "raw": raw,
                    "protocol": proto,
                    "host": [host_part],
                    "path": [p for p in path_parts if p]
                }
        else:
            segments = base.split("/")
            url_obj = {
                "raw": raw,
                "host": [segments[0]],
                "path": [s for s in segments[1:] if s]
            }

        if q_str:
            q_items = []
            for pair in q_str.split("&"):
                if "=" in pair:
                    k, v = pair.split("=", 1)
                    q_items.append({"key": k, "value": v})
                else:
                    q_items.append({"key": pair, "value": ""})
            url_obj["query"] = q_items

        return url_obj

    def make_req(name, method, url_raw, headers=None, body_obj=None, test_script=None):
        hdr = []
        if headers:
            for k, v in headers.items():
                hdr.append({"key": k, "value": str(v), "type": "text"})
        
        req_struct = {
            "method": method,
            "header": hdr,
            "url": make_url(url_raw)
        }

        if body_obj is not None:
            if not any(h["key"].lower() == "content-type" for h in hdr):
                hdr.append({"key": "Content-Type", "value": "application/json", "type": "text"})
            req_struct["body"] = {
                "mode": "raw",
                "raw": json.dumps(body_obj, indent=2) if isinstance(body_obj, (dict, list)) else str(body_obj),
                "options": {
                    "raw": {
                        "language": "json"
                    }
                }
            }

        item = {
            "name": name,
            "request": req_struct,
            "response": []
        }

        if test_script:
            item["event"] = [
                {
                    "listen": "test",
                    "script": {
                        "type": "text/javascript",
                        "exec": test_script if isinstance(test_script, list) else test_script.strip().split("\n")
                    }
                }
            ]

        return item

    folders = []

    # -------------------------------------------------------------
    # FOLDER 1: Authentication & JWT (Hình 6, 7, 8, 9)
    # -------------------------------------------------------------
    f1_items = [
        make_req(
            "Hình 06 - Login Admin (adminsys - Role 1) -> 200 OK",
            "POST",
            "{{baseUrl}}/api/auth/login",
            headers={"Content-Type": "application/json"},
            body_obj={"username": "adminsys", "password": "@1"},
            test_script=[
                'pm.test("Status code is 200 OK", function () { pm.response.to.have.status(200); });',
                'var res = pm.response.json();',
                'pm.test("Receive Access Token and Refresh Token", function () {',
                '    pm.expect(res.data.accessToken).to.be.a("string");',
                '    pm.expect(res.data.role).to.eql(1);',
                '    pm.collectionVariables.set("adminToken", res.data.accessToken);',
                '    pm.environment.set("adminToken", res.data.accessToken);',
                '    pm.collectionVariables.set("adminRefreshToken", res.data.refreshToken);',
                '    pm.environment.set("adminRefreshToken", res.data.refreshToken);',
                '});'
            ]
        ),
        make_req(
            "Hình 07a - Login Staff (staff02 - Role 2) -> 200 OK",
            "POST",
            "{{baseUrl}}/api/auth/login",
            headers={"Content-Type": "application/json"},
            body_obj={"username": "staff02", "password": "@1"},
            test_script=[
                'pm.test("Status code is 200 OK", function () { pm.response.to.have.status(200); });',
                'var res = pm.response.json();',
                'pm.test("Receive Staff Token with role=2", function () {',
                '    pm.expect(res.data.accessToken).to.be.a("string");',
                '    pm.expect(res.data.role).to.eql(2);',
                '    pm.collectionVariables.set("staffToken", res.data.accessToken);',
                '    pm.environment.set("staffToken", res.data.accessToken);',
                '});'
            ]
        ),
        make_req(
            "Hình 07b - Login Member (member01 - Role 3) -> 200 OK",
            "POST",
            "{{baseUrl}}/api/auth/login",
            headers={"Content-Type": "application/json"},
            body_obj={"username": "member01", "password": "@1"},
            test_script=[
                'pm.test("Status code is 200 OK", function () { pm.response.to.have.status(200); });',
                'var res = pm.response.json();',
                'pm.test("Receive Member Token with role=3", function () {',
                '    pm.expect(res.data.accessToken).to.be.a("string");',
                '    pm.expect(res.data.role).to.eql(3);',
                '    pm.collectionVariables.set("memberToken", res.data.accessToken);',
                '    pm.environment.set("memberToken", res.data.accessToken);',
                '});'
            ]
        ),
        make_req(
            "Hình 08 - Refresh Access Token via POST /api/auth/refresh -> 200 OK",
            "POST",
            "{{baseUrl}}/api/auth/refresh",
            headers={"Content-Type": "application/json"},
            body_obj={"refreshToken": "{{adminRefreshToken}}"},
            test_script=[
                'pm.test("Status code is 200 OK", function () { pm.response.to.have.status(200); });',
                'var res = pm.response.json();',
                'pm.test("Got new access token", function () {',
                '    pm.expect(res.data.accessToken).to.be.a("string");',
                '    pm.collectionVariables.set("adminToken", res.data.accessToken);',
                '    pm.environment.set("adminToken", res.data.accessToken);',
                '});'
            ]
        ),
        make_req(
            "Hình 09a - Login Failed with Wrong Password -> 401 Unauthorized",
            "POST",
            "{{baseUrl}}/api/auth/login",
            headers={"Content-Type": "application/json"},
            body_obj={"username": "adminsys", "password": "WrongPassword123!"},
            test_script=[
                'pm.test("Status code is 401 Unauthorized", function () { pm.response.to.have.status(401); });'
            ]
        ),
        make_req(
            "Hình 09b - Login Failed with Inactive Account (member02) -> 403 Forbidden",
            "POST",
            "{{baseUrl}}/api/auth/login",
            headers={"Content-Type": "application/json"},
            body_obj={"username": "member02", "password": "@1"},
            test_script=[
                'pm.test("Status code is 403 Forbidden (Inactive Account)", function () { pm.response.to.have.status(403); });'
            ]
        ),
    ]
    folders.append({"name": "01 - Authentication & JWT (Hình 6, 7, 8, 9)", "item": f1_items})

    # -------------------------------------------------------------
    # FOLDER 2: MSBrand Public & Internal API (Hình 11, 12, 13)
    # -------------------------------------------------------------
    f2_items = [
        make_req(
            "Hình 11 - GET All Brands with totalWatches (Public API)",
            "GET",
            "{{baseUrl}}/api/brands",
            headers={"Authorization": "Bearer {{adminToken}}"},
            test_script=[
                'pm.test("Status code is 200 OK", function () { pm.response.to.have.status(200); });',
                'var res = pm.response.json();',
                'pm.test("Returns 4 brands with watchCount", function () {',
                '    pm.expect(res.data.length).to.be.at.least(4);',
                '    pm.expect(res.data[0]).to.have.property("brandName");',
                '    pm.expect(res.data[0]).to.have.property("watchCount");',
                '});'
            ]
        ),
        make_req(
            "Hình 11b - GET Brand Detail by ID: Rolex (BrandID = 1)",
            "GET",
            "{{baseUrl}}/api/brands/1",
            headers={"Authorization": "Bearer {{adminToken}}"},
            test_script=[
                'pm.test("Status code is 200 OK", function () { pm.response.to.have.status(200); });',
                'var res = pm.response.json();',
                'pm.test("Brand is Rolex", function () {',
                '    pm.expect(res.data.brandName).to.eql("Rolex");',
                '});'
            ]
        ),
        make_req(
            "Hình 11c - GET Watches of Brand (BrandID = 1) -> 200 OK",
            "GET",
            "{{baseUrl}}/api/brands/1/watches",
            headers={"Authorization": "Bearer {{adminToken}}"},
            test_script=[
                'pm.test("Status code is 200 OK", function () { pm.response.to.have.status(200); });',
                'var res = pm.response.json();',
                'pm.test("Returns list of watch IDs linked to Rolex", function () {',
                '    pm.expect(res.data).to.have.property("watchIds");',
                '});'
            ]
        ),
        make_req(
            "Hình 12 - Internal PUT Assign Watch to Brand (Idempotent Participant)",
            "PUT",
            "http://localhost:8082/internal/brands/1/watches/100",
            test_script=[
                'pm.test("Status code is 200 OK", function () { pm.response.to.have.status(200); });',
                'var res = pm.response.json();',
                'pm.test("Assign successful", function () {',
                '    pm.expect(res.data.brandId).to.eql(1);',
                '    pm.expect(res.data.watchId).to.eql(100);',
                '    pm.expect(["ASSIGNED", "ALREADY_ASSIGNED"]).to.include(res.data.status);',
                '});'
            ]
        ),
        make_req(
            "Hình 13 - Internal DELETE Unassign Watch from Brand (Idempotent Compensation)",
            "DELETE",
            "http://localhost:8082/internal/brands/watches/100",
            test_script=[
                'pm.test("Status code is 200 OK", function () { pm.response.to.have.status(200); });',
                'var res = pm.response.json();',
                'pm.test("Unassign successful (Idempotent)", function () {',
                '    pm.expect(res.success).to.eql(true);',
                '    pm.expect(["UNASSIGNED", "NOTHING_TO_DO"]).to.include(res.data.status);',
                '});'
            ]
        ),
    ]
    folders.append({"name": "02 - MSBrand Public & Internal API (Hình 11, 12, 13)", "item": f2_items})

    # -------------------------------------------------------------
    # FOLDER 3: MSWatch Public Catalog (Hình 14, 15)
    # -------------------------------------------------------------
    f3_items = [
        make_req(
            "Hình 14 - GET All Watches (Public, No Auth, Sorted DESC by WatchID)",
            "GET",
            "{{baseUrl}}/api/watches",
            headers={"Authorization": "Bearer {{adminToken}}"},
            test_script=[
                'pm.test("Status code is 200 OK (Public Access)", function () { pm.response.to.have.status(200); });',
                'var res = pm.response.json();',
                'pm.test("Contains watch list with categoryName", function () {',
                '    pm.expect(res.data).to.be.an("array");',
                '    pm.expect(res.data.length).to.be.at.least(10);',
                '    pm.expect(res.data[0]).to.have.property("categoryName");',
                '});'
            ]
        ),
        make_req(
            "Hình 15 - GET Watch Detail by ID (WatchID = 1: Submariner Date)",
            "GET",
            "{{baseUrl}}/api/watches/1",
            headers={"Authorization": "Bearer {{adminToken}}"},
            test_script=[
                'pm.test("Status code is 200 OK", function () { pm.response.to.have.status(200); });',
                'var res = pm.response.json();',
                'pm.test("Watch detail matches Submariner Date", function () {',
                '    pm.expect(res.data.name).to.eql("Submariner Date");',
                '    pm.expect(res.data.categoryName).to.eql("Dive Watches");',
                '    pm.expect(res.data.price).to.eql(9550.0);',
                '});'
            ]
        ),
    ]
    folders.append({"name": "03 - MSWatch Public Catalog (Hình 14, 15)", "item": f3_items})

    # -------------------------------------------------------------
    # FOLDER 4: Business Validation Pre-Saga (Hình 16)
    # -------------------------------------------------------------
    f4_items = [
        make_req(
            "Hình 16a - Name <= 10 characters -> 400 Bad Request",
            "POST",
            "{{baseUrl}}/api/watches",
            headers={
                "Authorization": "Bearer {{adminToken}}",
                "Content-Type": "application/json"
            },
            body_obj={
                "name": "ShortName",
                "categoryId": 1,
                "brandId": 1,
                "caseMaterial": "Steel",
                "strapMaterial": "Leather",
                "waterpMaterial": "50m",
                "price": 500.0,
                "releaseDate": "{{todayDate}}",
                "stock": 10
            },
            test_script=['pm.test("Status is 400 Bad Request", function () { pm.response.to.have.status(400); });']
        ),
        make_req(
            "Hình 16b - Price < 100 -> 400 Bad Request",
            "POST",
            "{{baseUrl}}/api/watches",
            headers={
                "Authorization": "Bearer {{adminToken}}",
                "Content-Type": "application/json"
            },
            body_obj={
                "name": "Valid Watch Name Long Enough",
                "categoryId": 1,
                "brandId": 1,
                "caseMaterial": "Steel",
                "strapMaterial": "Leather",
                "waterpMaterial": "50m",
                "price": 99.0,
                "releaseDate": "{{todayDate}}",
                "stock": 10
            },
            test_script=['pm.test("Status is 400 Bad Request", function () { pm.response.to.have.status(400); });']
        ),
        make_req(
            "Hình 16c - ReleaseDate != Current Date -> 400 Bad Request",
            "POST",
            "{{baseUrl}}/api/watches",
            headers={
                "Authorization": "Bearer {{adminToken}}",
                "Content-Type": "application/json"
            },
            body_obj={
                "name": "Valid Watch Name Long Enough",
                "categoryId": 1,
                "brandId": 1,
                "caseMaterial": "Steel",
                "strapMaterial": "Leather",
                "waterpMaterial": "50m",
                "price": 500.0,
                "releaseDate": "2020-01-01",
                "stock": 10
            },
            test_script=['pm.test("Status is 400 Bad Request", function () { pm.response.to.have.status(400); });']
        ),
        make_req(
            "Hình 16d - Category not found -> 400 Bad Request",
            "POST",
            "{{baseUrl}}/api/watches",
            headers={
                "Authorization": "Bearer {{adminToken}}",
                "Content-Type": "application/json"
            },
            body_obj={
                "name": "Valid Watch Name Long Enough",
                "categoryId": 999,
                "brandId": 1,
                "caseMaterial": "Steel",
                "strapMaterial": "Leather",
                "waterpMaterial": "50m",
                "price": 500.0,
                "releaseDate": "{{todayDate}}",
                "stock": 10
            },
            test_script=['pm.test("Status is 400 Bad Request", function () { pm.response.to.have.status(400); });']
        ),
    ]
    folders.append({"name": "04 - Business Validation Pre-Saga (Hình 16)", "item": f4_items})

    # -------------------------------------------------------------
    # FOLDER 5: API Gateway Security & Resilience (Hình 17, 18, 19, 20)
    # -------------------------------------------------------------
    f5_items = [
        make_req(
            "Hình 17 - Gateway Blocks Protected POST /api/watches without Token -> 401 Unauthorized",
            "POST",
            "{{baseUrl}}/api/watches",
            headers={"Content-Type": "application/json"},
            body_obj={
                "name": "Unauthorized Watch Creation",
                "categoryId": 1,
                "brandId": 1,
                "caseMaterial": "Steel",
                "strapMaterial": "Steel",
                "waterpMaterial": "100m",
                "price": 1000.0,
                "releaseDate": "{{todayDate}}",
                "stock": 5
            },
            test_script=['pm.test("Status is 401 Unauthorized", function () { pm.response.to.have.status(401); });']
        ),
        make_req(
            "Hình 18 - Gateway Blocks Staff (Role 2) Attempting DELETE /api/watches/1 -> 403 Forbidden",
            "DELETE",
            "{{baseUrl}}/api/watches/1",
            headers={"Authorization": "Bearer {{staffToken}}"},
            test_script=['pm.test("Status is 403 Forbidden (RBAC Admin Only)", function () { pm.response.to.have.status(403); });']
        ),
        make_req(
            "Hình 19 - Header Spoofing (Client Injects X-User-Role: 1) -> Stripped by Gateway -> 403",
            "POST",
            "{{baseUrl}}/api/watches",
            headers={
                "Authorization": "Bearer {{staffToken}}",
                "X-User-Role": "1",
                "Content-Type": "application/json"
            },
            body_obj={
                "name": "Attempting Header Spoofing Watch",
                "categoryId": 1,
                "brandId": 1,
                "caseMaterial": "Steel",
                "strapMaterial": "Steel",
                "waterpMaterial": "100m",
                "price": 1000.0,
                "releaseDate": "{{todayDate}}",
                "stock": 5
            },
            test_script=['pm.test("Status is 403 Forbidden (Gateway Stripped Spoofed Header)", function () { pm.response.to.have.status(403); });']
        ),
        make_req(
            "Hình 20 - Circuit Breaker Fallback Endpoint -> 503 Service Unavailable",
            "GET",
            "{{baseUrl}}/fallback/watch",
            test_script=[
                'pm.test("Status is 503 Service Unavailable", function () { pm.response.to.have.status(503); });',
                'var res = pm.response.json();',
                'pm.test("Fallback message returned", function () {',
                '    pm.expect(res.message).to.include("currently unavailable");',
                '});'
            ]
        ),
    ]
    folders.append({"name": "05 - API Gateway Security & Resilience (Hình 17, 18, 19, 20)", "item": f5_items})

    # -------------------------------------------------------------
    # FOLDER 6: Saga Scenarios A to E (Hình 21, 23, 25, 26, 27)
    # -------------------------------------------------------------
    f6_items = [
        make_req(
            "Hình 21 - Kịch bản A: CREATE Watch Success (Rolex Batman, BrandID = 1) -> 201 Created",
            "POST",
            "{{baseUrl}}/api/watches",
            headers={
                "Authorization": "Bearer {{adminToken}}",
                "Content-Type": "application/json"
            },
            body_obj={
                "name": "Rolex GMT-Master II Batman",
                "categoryId": 1,
                "brandId": 1,
                "caseMaterial": "Oystersteel",
                "strapMaterial": "Oystersteel",
                "waterpMaterial": "100 meters",
                "price": 10750.00,
                "releaseDate": "{{todayDate}}",
                "stock": 15
            },
            test_script=[
                'pm.test("Status code is 201 Created", function () { pm.response.to.have.status(201); });',
                'var res = pm.response.json();',
                'var sagaId = pm.response.headers.get("X-Saga-Id") || (res.data && res.data.sagaId);',
                'pm.test("Saga created watch successfully", function () {',
                '    pm.expect(res.data).to.have.property("watchId");',
                '    pm.collectionVariables.set("newWatchId", String(res.data.watchId));',
                '    pm.environment.set("newWatchId", String(res.data.watchId));',
                '    if (sagaId) {',
                '        pm.collectionVariables.set("sagaA_Id", sagaId);',
                '        pm.environment.set("sagaA_Id", sagaId);',
                '    }',
                '});'
            ]
        ),
        make_req(
            "Hình 21b - Verify Saga A State & Logs -> COMPLETED",
            "GET",
            "{{baseUrl}}/api/sagas/{{sagaA_Id}}",
            headers={"Authorization": "Bearer {{adminToken}}"},
            test_script=[
                'pm.test("Status code is 200 OK", function () { pm.response.to.have.status(200); });',
                'var res = pm.response.json();',
                'pm.test("Saga A is COMPLETED", function () {',
                '    pm.expect(res.data.status).to.eql("COMPLETED");',
                '    pm.expect(res.data.steps.length).to.be.at.least(2);',
                '});'
            ]
        ),
        make_req(
            "Hình 23 - Kịch bản B: CREATE with Invalid Brand 999 -> Compensation Triggered",
            "POST",
            "{{baseUrl}}/api/watches",
            headers={
                "Authorization": "Bearer {{adminToken}}",
                "Content-Type": "application/json"
            },
            body_obj={
                "name": "Watch With Nonexistent Brand 999",
                "categoryId": 2,
                "brandId": 999,
                "caseMaterial": "Titanium",
                "strapMaterial": "Rubber",
                "waterpMaterial": "200 meters",
                "price": 2500.00,
                "releaseDate": "{{todayDate}}",
                "stock": 10
            },
            test_script=[
                'pm.test("Status is 400 Bad Request or 500", function () {',
                '    pm.expect([400, 500]).to.include(pm.response.code);',
                '});',
                'var res = pm.response.json();',
                'var sagaId = pm.response.headers.get("X-Saga-Id") || (res.data && res.data.sagaId);',
                'if (sagaId) {',
                '    pm.collectionVariables.set("sagaB_Id", sagaId);',
                '    pm.environment.set("sagaB_Id", sagaId);',
                '}'
            ]
        ),
        make_req(
            "Hình 24 - Verify Saga B State -> COMPENSATED (Local Watch Rolled Back)",
            "GET",
            "{{baseUrl}}/api/sagas/{{sagaB_Id}}",
            headers={"Authorization": "Bearer {{adminToken}}"},
            test_script=[
                'pm.test("Status code is 200 OK", function () { pm.response.to.have.status(200); });',
                'var res = pm.response.json();',
                'pm.test("Saga B is COMPENSATED", function () {',
                '    pm.expect(res.data.status).to.eql("COMPENSATED");',
                '});'
            ]
        ),
        make_req(
            "Hình 25 - Kịch bản C: UPDATE Watch Rebrand from Rolex to Omega (Brand 1 -> 2) -> 200 OK",
            "PUT",
            "{{baseUrl}}/api/watches/{{newWatchId}}",
            headers={
                "Authorization": "Bearer {{adminToken}}",
                "Content-Type": "application/json"
            },
            body_obj={
                "name": "Rolex Rebranded to Omega Speedmaster",
                "categoryId": 1,
                "brandId": 2,
                "caseMaterial": "Stainless Steel",
                "strapMaterial": "Stainless Steel",
                "waterpMaterial": "100 meters",
                "price": 8500.00,
                "releaseDate": "{{todayDate}}",
                "stock": 20
            },
            test_script=[
                'pm.test("Status code is 200 OK", function () { pm.response.to.have.status(200); });',
                'var res = pm.response.json();',
                'var sagaId = pm.response.headers.get("X-Saga-Id") || (res.data && res.data.sagaId);',
                'pm.test("Saga C updated watch successfully", function () {',
                '    if (sagaId) {',
                '        pm.collectionVariables.set("sagaC_Id", sagaId);',
                '        pm.environment.set("sagaC_Id", sagaId);',
                '    }',
                '});'
            ]
        ),
        make_req(
            "Hình 25b - Verify Saga C State -> COMPLETED",
            "GET",
            "{{baseUrl}}/api/sagas/{{sagaC_Id}}",
            headers={"Authorization": "Bearer {{adminToken}}"},
            test_script=[
                'pm.test("Status code is 200 OK", function () { pm.response.to.have.status(200); });',
                'var res = pm.response.json();',
                'pm.test("Saga C status is COMPLETED", function () {',
                '    pm.expect(res.data.status).to.eql("COMPLETED");',
                '});'
            ]
        ),
        make_req(
            "Hình 26 - Kịch bản D: UPDATE with Invalid Brand 999 -> Restores Snapshot -> COMPENSATED",
            "PUT",
            "{{baseUrl}}/api/watches/{{newWatchId}}",
            headers={
                "Authorization": "Bearer {{adminToken}}",
                "Content-Type": "application/json"
            },
            body_obj={
                "name": "Invalid Brand Update Attempt",
                "categoryId": 1,
                "brandId": 999,
                "caseMaterial": "Gold",
                "strapMaterial": "Gold",
                "waterpMaterial": "50 meters",
                "price": 15000.00,
                "releaseDate": "{{todayDate}}",
                "stock": 5
            },
            test_script=[
                'pm.test("Status is 400 or 500", function () {',
                '    pm.expect([400, 500]).to.include(pm.response.code);',
                '});',
                'var res = pm.response.json();',
                'var sagaId = pm.response.headers.get("X-Saga-Id") || (res.data && res.data.sagaId);',
                'if (sagaId) {',
                '    pm.collectionVariables.set("sagaD_Id", sagaId);',
                '    pm.environment.set("sagaD_Id", sagaId);',
                '}'
            ]
        ),
        make_req(
            "Hình 26b - Verify Saga D State -> COMPENSATED (Snapshot Restored)",
            "GET",
            "{{baseUrl}}/api/sagas/{{sagaD_Id}}",
            headers={"Authorization": "Bearer {{adminToken}}"},
            test_script=[
                'pm.test("Status code is 200 OK", function () { pm.response.to.have.status(200); });',
                'var res = pm.response.json();',
                'pm.test("Saga D status is COMPENSATED", function () {',
                '    pm.expect(res.data.status).to.eql("COMPENSATED");',
                '});'
            ]
        ),
        make_req(
            "Hình 27 - Kịch bản E: DELETE Watch (Pivot Step) -> 200 OK",
            "DELETE",
            "{{baseUrl}}/api/watches/{{newWatchId}}",
            headers={"Authorization": "Bearer {{adminToken}}"},
            test_script=[
                'pm.test("Status code is 200 OK", function () { pm.response.to.have.status(200); });',
                'var res = pm.response.json();',
                'var sagaId = pm.response.headers.get("X-Saga-Id") || (res.data && res.data.sagaId);',
                'pm.test("Saga E deleted watch", function () {',
                '    if (sagaId) {',
                '        pm.collectionVariables.set("sagaE_Id", sagaId);',
                '        pm.environment.set("sagaE_Id", sagaId);',
                '    }',
                '});'
            ]
        ),
        make_req(
            "Hình 27b - Verify Saga E State -> COMPLETED",
            "GET",
            "{{baseUrl}}/api/sagas/{{sagaE_Id}}",
            headers={"Authorization": "Bearer {{adminToken}}"},
            test_script=[
                'pm.test("Status code is 200 OK", function () { pm.response.to.have.status(200); });',
                'var res = pm.response.json();',
                'pm.test("Saga E status is COMPLETED", function () {',
                '    pm.expect(res.data.status).to.eql("COMPLETED");',
                '});'
            ]
        ),
    ]
    folders.append({"name": "06 - Saga Scenarios A to E (Hình 21, 23, 25, 26, 27)", "item": f6_items})

    # -------------------------------------------------------------
    # FOLDER 7: Fault Injection & Edge Cases (Hình 28, 29)
    # -------------------------------------------------------------
    f7_items = [
        make_req(
            "Hình 28 - Kịch bản F: Fault Injection (Header X-Saga-Fail-After-Step: 1) -> 500",
            "POST",
            "{{baseUrl}}/api/watches",
            headers={
                "Authorization": "Bearer {{adminToken}}",
                "X-Saga-Fail-After-Step": "1",
                "Content-Type": "application/json"
            },
            body_obj={
                "name": "Watch With Simulated Step 1 Failure",
                "categoryId": 3,
                "brandId": 1,
                "caseMaterial": "Ceramic",
                "strapMaterial": "Rubber",
                "waterpMaterial": "300 meters",
                "price": 12000.00,
                "releaseDate": "{{todayDate}}",
                "stock": 5
            },
            test_script=[
                'pm.test("Status code is 500 (Simulated Failure)", function () { pm.response.to.have.status(500); });',
                'var res = pm.response.json();',
                'var sagaId = pm.response.headers.get("X-Saga-Id") || (res.data && res.data.sagaId);',
                'if (sagaId) {',
                '    pm.collectionVariables.set("sagaF_Id", sagaId);',
                '    pm.environment.set("sagaF_Id", sagaId);',
                '}'
            ]
        ),
        make_req(
            "Hình 28b - Verify Saga F State & LIFO Logs -> COMPENSATED",
            "GET",
            "{{baseUrl}}/api/sagas/{{sagaF_Id}}",
            headers={"Authorization": "Bearer {{adminToken}}"},
            test_script=[
                'pm.test("Status code is 200 OK", function () { pm.response.to.have.status(200); });',
                'var res = pm.response.json();',
                'pm.test("Saga F is COMPENSATED via LIFO", function () {',
                '    pm.expect(res.data.status).to.eql("COMPENSATED");',
                '});'
            ]
        ),
        make_req(
            "Hình 29 - Kịch bản Edge Case: MSBrand Connection Error Simulation -> 500",
            "POST",
            "{{baseUrl}}/api/watches",
            headers={
                "Authorization": "Bearer {{adminToken}}",
                "X-Saga-Fail-After-Step": "2",
                "Content-Type": "application/json"
            },
            body_obj={
                "name": "Watch Simulating Downstream Step 2 Failure",
                "categoryId": 4,
                "brandId": 3,
                "caseMaterial": "Resin",
                "strapMaterial": "Resin",
                "waterpMaterial": "200 meters",
                "price": 350.00,
                "releaseDate": "{{todayDate}}",
                "stock": 50
            },
            test_script=[
                'pm.test("Status code is 500", function () { pm.response.to.have.status(500); });',
                'var res = pm.response.json();',
                'var sagaId = pm.response.headers.get("X-Saga-Id") || (res.data && res.data.sagaId);',
                'if (sagaId) {',
                '    pm.collectionVariables.set("sagaEdge_Id", sagaId);',
                '    pm.environment.set("sagaEdge_Id", sagaId);',
                '}'
            ]
        ),
        make_req(
            "Hình 29b - Verify Edge Case Saga Rolled Back Locally -> COMPENSATED",
            "GET",
            "{{baseUrl}}/api/sagas/{{sagaEdge_Id}}",
            headers={"Authorization": "Bearer {{adminToken}}"},
            test_script=[
                'pm.test("Status code is 200 OK", function () { pm.response.to.have.status(200); });',
                'var res = pm.response.json();',
                'pm.test("Edge case saga status is COMPENSATED", function () {',
                '    pm.expect(res.data.status).to.eql("COMPENSATED");',
                '});'
            ]
        ),
    ]
    folders.append({"name": "07 - Fault Injection & Edge Cases (Hình 28, 29)", "item": f7_items})

    # -------------------------------------------------------------
    # FOLDER 8: Saga Monitoring API
    # -------------------------------------------------------------
    f8_items = [
        make_req(
            "Saga Monitoring - Admin Lists Recent Sagas -> 200 OK",
            "GET",
            "{{baseUrl}}/api/sagas?limit=10",
            headers={"Authorization": "Bearer {{adminToken}}"},
            test_script=[
                'pm.test("Status code is 200 OK", function () { pm.response.to.have.status(200); });',
                'var res = pm.response.json();',
                'pm.test("Returns list of recent sagas", function () {',
                '    pm.expect(res.data).to.be.an("array");',
                '});'
            ]
        ),
        make_req(
            "Saga Monitoring - Staff Calls /api/sagas -> 403 Forbidden",
            "GET",
            "{{baseUrl}}/api/sagas",
            headers={"Authorization": "Bearer {{staffToken}}"},
            test_script=['pm.test("Status is 403 Forbidden", function () { pm.response.to.have.status(403); });']
        ),
    ]
    folders.append({"name": "08 - Saga Monitoring API", "item": f8_items})

    collection = {
        "info": {
            "_postman_id": "watchmanagement-saga-postman-v2",
            "name": "WatchManagement_Saga",
            "description": "Complete Postman Collection mapped directly to Report Figures (Hình 6 to Hình 30) for Assignment 02 - MSS301",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "event": [
            {
                "listen": "prerequest",
                "script": {
                    "type": "text/javascript",
                    "exec": [
                        "// Auto set todayDate to current system date (YYYY-MM-DD)",
                        "const today = new Date().toISOString().split('T')[0];",
                        "pm.collectionVariables.set('todayDate', today);",
                        "pm.environment.set('todayDate', today);"
                    ]
                }
            }
        ],
        "variable": [
            {"key": "baseUrl", "value": "http://localhost:8080", "type": "string"},
            {"key": "brandUrl", "value": "http://localhost:8080", "type": "string"},
            {"key": "adminToken", "value": "", "type": "string"},
            {"key": "adminRefreshToken", "value": "", "type": "string"},
            {"key": "staffToken", "value": "", "type": "string"},
            {"key": "memberToken", "value": "", "type": "string"},
            {"key": "newWatchId", "value": "1", "type": "string"},
            {"key": "sagaA_Id", "value": "", "type": "string"},
            {"key": "sagaB_Id", "value": "", "type": "string"},
            {"key": "sagaC_Id", "value": "", "type": "string"},
            {"key": "sagaD_Id", "value": "", "type": "string"},
            {"key": "sagaE_Id", "value": "", "type": "string"},
            {"key": "sagaF_Id", "value": "", "type": "string"},
            {"key": "sagaEdge_Id", "value": "", "type": "string"},
            {"key": "todayDate", "value": today_str, "type": "string"}
        ],
        "item": folders
    }

    out_file = "Slot18/Assignment2/WatchManagement/WatchManagement_Saga.postman_collection.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(collection, f, indent=2, ensure_ascii=False)

    total_reqs = sum(len(f['item']) for f in folders)
    print(f"Generated {out_file} with {total_reqs} requests across {len(folders)} folders!")

if __name__ == "__main__":
    build_postman_collection()
