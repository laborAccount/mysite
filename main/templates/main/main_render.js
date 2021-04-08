<script id="inviteTemplate" type="text/x-jsrender">
<div style="text-align: center;">
		<table style="display: inline-block; width:100%; margin-bottom: 20px;" id="callInfoTable">
					<tbody>
							<tr>
									<td>Conference name</td>
									<td class="rightTd" style="width:100%;"><input type="text" class="form-control" data-id="conferencename" id="conferencename" placeholder="" value="{{:endCallDetail[0].name}}"></td>
							</tr>
							<tr>
									<td>callID</td>
									<td class="rightTd"><input type="number" min="1" max="99999999" class="form-control" data-id="callid" id="callid" placeholder="숫자 8자 까지 입력 가능합니다" value="{{:endCallDetail[0].call_id}}"></td>
							</tr>
							<tr>
									<td>uri</td>
									<td class="rightTd"><input type="number" min="1" max="99999999" class="form-control" data-id="uri" id="uri" placeholder="숫자 8자 까지 입력 가능합니다" value="{{:endCallDetail[0].uri}}"></td>
							</tr>
							<input type="hidden" data-id="cospaceid" id="cospaceid" value="{{:endCallDetail[0].cospace}}" >
					</tbody>
		</table>
</div>
  <!----------------------- user - -------------------------->
  <div style="width:340px; float:left; margin-right: 40px;">
    <span class="nav-icon" style="padding-bottom: 18px;">
      <i class="fa fa-address-book-o"></i>
    </span>
    <div>
      <strong>User</strong>
    </div>
    <div class="table-responsive detail_table_acanoClient" style="width: 340px;  height:400px;">
      <table class="table table-hover table-striped table-bordered" id="detail_table_acanoClient" style="width:100%; height: 247px;">
        <thead>
          <tr>
            <th class="th-center" style="width: 5%;" width="5%"><input type="checkbox" id="select_all_user"/></th>
            <th class="th-center"style="width: 5%;" hidden>user_id</th>
            <th class="th-center" style="width: 35%;" width="35%">Name</th>
            <th class="th-center" style="width: 60%" width="60%">User JID</th>
          </tr>
        </thead>
        <tbody>
          {{for userlist}}
            <tr>
              <td style="width: 5%;" width="5%" class="userCheck"><input type="checkbox"></td>
              <td hidden>{{:user_id}}</td>
              <td style="width: 35%;" width="35%">{{:name}}</td>
              <td style="width: 60%;" width="60%" class="userJid">{{:userJid}}</td>
            </tr>
          {{/for}}
        </tbody>
      </table>
    </div>
  </div>
  <!----------------------- user - -------------------------->

  <!----------------------- endpoint - -------------------------->
  <div class="table-responsive" style="width: 470px;">
    <span class="nav-icon"  style="padding-bottom: 18px;">
      <i class="fa fa-address-book-o"></i>
    </span>
    <div>
      <strong>Endpoint</strong>
    </div>
    <div class="table-responsive detail_table_endPoint" style="width: 460px;  height:400px;">
      <table class="table table-hover table-striped table-bordered" id="detail_table_endPoint" style="width:100%; height: 247px;">
        <thead>
          <tr>
            <th class="th-center" style="width: 5%;"><input type="checkbox" id="select_all_ep"/></th>
            <th class="th-center" hidden>EndPoint id</th>
            <th class="th-center" style="width: 30%;" width="30%">EndPoint Name</th>
            <th class="th-center" style="width: 15%;" width="15%">Type</th>
            <th class="th-center" style="width: 30%;" width="30%">CallNumber</th>
            <th class="th-center" style="width: 20%;" width="20%">Group</th>
          </tr>
        </thead>
        <tbody>
          {{for eplist}}
            <tr>
              <td width="5%" class="endCheck"><input type="checkbox"></td>
              <td hidden>{{:ep_id}}</td>
              <td width="30%">{{:ep_name}}</td>
              <td width="15%">{{:ep_type}}</td>
              <td width="30%" class="callNumber">{{:ip}}</td>
              <td width="20%">{{:ep_group_name}}</td>
            </tr>
          {{/for}}
        </tbody>
      </table>
    </div>
  </div>
  <!----------------------- endpoint - ---------------------------->
  </script>
