;(function($){

    var _default_bandwidth = _api_json.settings.default_bandwidth;
  
    var _tableWeb;
    var _tableMerge;
    var _tableEp;
  
    var _mergeSeq = 0;
    var _mergeWebList = [];
    var _mergeEpList = [];
  
    var _bandwidthValList = ['64000', '128000', '192000', '256000', '320000', '384000', '512000', '768000',
      '1000000', '1250000', '1500000', '1750000', '2000000', '2500000', '3000000', '3500000',
      '4000000',  '5000000', '6000000'];
  
    var _bandwidthKeyList = [
      '64k', '128k', '192k', '256k', '320k', '384k', '512k', '768k', '1.00M', '1.25M', '1.50M', '1.75M', '2.00M', '2.50M',
      '3.00M', '3.50M', '4.00M', '5.00M', '6.00M'
    ];
  
    // ---------------------------- EndPoint ----------------------------
    // EndPoint 테이블 초기화
    $.fn.createEpTable = function() {
      var _this = $(this);
  
      _tableEp = _this.DataTable({
        dom: '<"row"<"col-sm-6 tm-text-group-endpoint"f>""<"col-sm-6 tm-btn-group-endpoint text-right">">t<"row"<"col-sm-12"p>>',
        searching: false,
        paginate: true,
        pageLength: 5,
        processing: true,
        serverSide: true,
        ordering: false,
        ajax: {
          url: "/endpoint/list",
          type: "POST",
          dataType: "json",
          data: function (d) {
            d.searchText = (typeof($("#epSearch").val())=="undefined") ? "" : $("#epSearch").val();
            d.csrfmiddlewaretoken = $('.hidden_csrftoken').val();
          },
          dataFilter: function (data) {
            var json = jQuery.parseJSON(data);
            return JSON.stringify(json);
          }
        },
        columns: [
          {data: 'ep_id', className:'text-center text-middle sel-check', fnCreatedCell:function(nTd, sData, oData, iRow, iCol){
            $(nTd).html($.dtcheckboxbs4());
          }},
          {data: 'ep_name'},
          {data: 'ep_type'},
          {data: 'callNumber'},
          {data: 'ep_group_name'},
          {data: 'bandwidth'}
        ],
        columnDefs: [
          {targets: 0, orderable: false, searchable: false, checkboxes: true, className: "text-center text-middle"},
          {targets: [2,5], orderable: false, searchable: false, visible: false},
          {targets: [1, 2, 3, 4, 5], className: "text-center text-middle"}
        ],
        initComplete: function () {
  
          var epSearchBox = $("<input>").attr({"type":"text","id":"epSearch"})
                                      .addClass(["form-control","dis-inline-block","m-r-2","tm-w-40"])
                                      .attr("placeholder","Search")
                                      .unbind()
                                      .bind('keyup',function(e){
                                        if (e.keyCode == 13) {
                                          _tableEp.search(this.value).draw();
                                        }
                                      });
  
          var epTitle = $("<h5>").text(gettext("common.invite.endpointlist"));
  
          $(".tm-btn-group-endpoint").append(epSearchBox);
          $(".tm-text-group-endpoint").append(epTitle);
  
          _epTableClickEvent(_this.find("thead"));
  
        },
        drawCallback:function(){
  
          _epTableClickEvent(_this.find("tbody"));
  
          // 체크박스 정리 이벤트
          for(var i=_tableEp.rows().data().length-1;i>=0;i--){
            var epCheckFlag = true;
            for(var j=_mergeEpList.length-1;j>=0;j--){
              if(_tableEp.rows().data()[i]['callNumber'] == _mergeEpList[j]['remoteParty']){
                _tableEp.cell(i,0).checkboxes.select();
                epCheckFlag = false;
  
                break;
              }
            }
            if(epCheckFlag){
              _tableEp.cell(i,0).checkboxes.deselect();
            }
          }
  
        }
      }).columns.adjust();
  
      $(this).find("thead > tr > th > input[type='checkbox']").parent().html($.dtcheckboxbs4head());
  
      return _tableEp;
  
    }
  
    // EndPoint 테이블 클릭 이벤트
    function _epTableClickEvent(ele){
      $(ele).find(".sel-check > label > input").each(function(){
        $(this).unbind().on("change",function(){
            var epCheck = $(this).prop("checked");
            if(epCheck){
              _epTableAdd();
            }else{
              _epTableCheckRemove();
            }
        });
      });
    }
  
    // EndPoint 테이블 ADD 버튼 이벤트
    function _epTableAdd() {
  
      var epAddChkList = [];
      var epAddSelList = [];
      var epAddParamList = [];
  
      var epAddDataList = _tableEp.column(0).checkboxes.selected();
  
      $.each(epAddDataList, function (key, value) {
        epAddChkList.push(value);
      });
  
      var table_data = _tableEp.rows().column(0).data();
  
      for (var j = 0; j < epAddChkList.length; j++) {
        for (var i = 0; i < table_data.length; i++) {
          if (table_data[i] == epAddChkList[j]) {
            epAddSelList.push(i);
            break;
          }
        }
      }
  
      for (var i = 0; i < epAddSelList.length; i++) {
  
        var epAddTableData = _tableEp.row(epAddSelList[i]).data();
        var epAddTemp = {};
            epAddTemp['t_seq'] = _mergeSeq;
            epAddTemp['ep_id'] = epAddTableData['ep_id'];
            epAddTemp['name'] = epAddTableData['ep_name'];
            epAddTemp['remoteParty'] = epAddTableData['callNumber'];
            epAddTemp['ep_group_name'] = epAddTableData['ep_group_name'];
            epAddTemp['bandwidth'] = epAddTableData['bandwidth'];
            epAddTemp['devicetype'] = 'EP';
  
        _mergeSeq = _mergeSeq + 1;
        
        var epAddTempFlag = true;
        for(var j=0;j<_mergeEpList.length;j++){
          if(_mergeEpList[j]['remoteParty'] == epAddTemp['remoteParty'] && _mergeEpList[j]['name'] == epAddTemp['name']){
            epAddTempFlag = false;
            break;
          }
        }
  
        if(epAddTempFlag){
          _mergeEpList.push(epAddTemp);
        }
        
        epAddParamList.push(epAddTemp);
  
      }
  
      _dataMerge(epAddParamList);
  
    }
  
    // EndPOint 테이블 체크박스 제거시 이벤트
    function _epTableCheckRemove(){
  
      var epDelChkList = []; // 체크목록
      var epDelPageData = []; // 페이지 데이터
  
      // Step1. 해당 페이지 데이터 로드
      var epDelList = _tableEp.column(0).checkboxes.selected();
  
      $.each(_tableEp.rows().data(),function(){
        $(this)[0]['devicetype'] = "EP";
        epDelPageData.push($(this)[0]);
      });
  
      // Step2. 체크 데이터 목록
      $.each(epDelList, function (key, value) {
        epDelChkList.push(value);
      });
  
      // Step3. 페이지 데이터 - 체크 데이터
      for(var i=epDelPageData.length-1; i>=0 ; i--){
        for(var j=0;j<epDelChkList.length;j++){
          if(epDelPageData[i]["ep_id"] == epDelChkList[j]){
            epDelPageData.splice(i,1);
            break;
          }
        }
      }
  
      for(var i=_mergeEpList.length-1; i>=0; i--){
        for(var j=0;j<epDelPageData.length;j++){
          if(_mergeEpList[i]['remoteParty'] == epDelPageData[j]['callNumber']){
            _mergeEpList.splice(i,1);
            break;
          }
        }
      }
  
      // Step4. Merge Table 데이터 삭제
      _mergeDataRemove(epDelPageData);
  
    }
    
    // ---------------------------- Merge ----------------------------
    $.fn.createMergeTable = function() {
      var _this = $(this);
  
      _tableMerge = _this.DataTable({
        dom: '<"row"<"col-sm-6 tm-text-group-merge"f>""<"col-sm-6 tm-btn-group-merge text-right">">t<"row"<"col-sm-12"p>>',
        searching: false,
        paginate: false,
        ordering: false,
        destroy: true,
        scrollY: "260px",
        columns: [
          {data: 't_seq', className:'text-center text-middle sel-check', fnCreatedCell:function(nTd, sData, oData, iRow, iCol){
            $(nTd).html($.dtcheckboxbs4());
          }},
          {data: 'name'},
          {
            data: 'remoteParty',
            defaultContent: '',
            name: 'remoteParty',
            fnCreatedCell: function (nTd, sData, oData, iRow, iCol) {
              $(nTd).html("<input type='text' class='remoteParty form-control' data-key='remoteParty'>");
            }
          },
          {data: 'ep_group_name'},
          {
            data: 'bandwidth',
            defaultContent: '',
            name: 'bandwidth',
            fnCreatedCell: function (nTd, sData, oData, iRow, iCol) {
  
              var _select = $("<select>").addClass('bandwidth custom-select w-100').attr('data-key','bandwidth');
  
              for(var i = 0; i < _bandwidthValList.length; i++){
                var _option = $("<option>").val(_bandwidthValList[i]).html(_bandwidthKeyList[i]);
                _select.append(_option);
              }
  
              if(sData != ''){
                $(nTd).html(_select.val(sData));
              }else{
                $(nTd).html(_select);
              }
  
            }
          },
          {
            data: 'dtmf',
            defaultContent: '',
            name: 'dtmf',
            fnCreatedCell: function (nTd, sData, oData, iRow, iCol) {
              var dtmf = $("<input>").attr("type","text")
                                     .attr("data-key","dtmf")
                                     .addClass(["dtmf","form-control"]);
  
              $(nTd).html(dtmf);
            }
          },
          {
            data: 'nameLabelOverride',
            defaultContent: '',
            name: 'nameLabelOverride',
            fnCreatedCell: function (nTd, sData, oData, iRow, iCol) {
              var nameLabelOverride = $("<input>").attr("type","text")
                                                  .attr("data-key","nameLabelOverride")
                                                  .addClass(["nameLabel","form-control"]);
  
              $(nTd).html(nameLabelOverride);
            }
          },
          {
            data: 'qualityMain',
            defaultContent: 'unrestricted',
            name: 'qualityMain',
            fnCreatedCell: function (nTd, sData, oData, iRow, iCol) {
              var quailtyMain = $("<select>").addClass("qualityMain custom-select")
                                             .attr("data-key","qualityMain")
                                             .append("<option val='unrestricted'>unrestricted</option>")
                                             .append("<option val='max1080p30'>max1080p30</option>")
                                             .append("<option val='max720p30'>max720p30</option>")
                                             .append("<option val='max480p30'>max480p30</option>");
  
              $(nTd).html(quailtyMain);
            }
          },
          {
            data: 'qualityPresentation',
            defaultContent: 'unrestricted',
            name: 'qualityPresentation',
            fnCreatedCell: function (nTd, sData, oData, iRow, iCol) {
              var qualityPresentation = $("<select class='qualityPresentation custom-select'>").attr("data-key","qualityPresentation")
                                                                                               .append("<option val='unrestricted'>unrestricted</option>")
                                                                                               .append("<option val='max1080p30'>max1080p30</option>")
                                                                                               .append("<option val='max720p5'>max720p5</option>");
              $(nTd).html(qualityPresentation);
            }
          },
          {data: 't_seq', name: 'rxAudioMute',fnCreatedCell:function(nTd, sData, oData, iRow, iCol){
            var $temp = $($(nTd).html($.dtcheckboxbs4())).find("input[type='checkbox']");
            return $temp.attr("data-key","rxAudioMute");
          }},
          {data: 't_seq', name: 'txAudioMute',fnCreatedCell:function(nTd, sData, oData, iRow, iCol){
            var $temp = $($(nTd).html($.dtcheckboxbs4())).find("input[type='checkbox']");
            return $temp.attr("data-key","txAudioMute");
          }},
          {data: 't_seq', name: 'rxVideoMute',fnCreatedCell:function(nTd, sData, oData, iRow, iCol){
            var $temp = $($(nTd).html($.dtcheckboxbs4())).find("input[type='checkbox']");
            return $temp.attr("data-key","rxVideoMute");
          }},
          {data: 't_seq', name: 'txVideoMute',fnCreatedCell:function(nTd, sData, oData, iRow, iCol){
            var $temp = $($(nTd).html($.dtcheckboxbs4())).find("input[type='checkbox']");
            return $temp.attr("data-key","txVideoMute");
          }},
          {data: 't_seq', name: 'presentationContributionAllowed',fnCreatedCell:function(nTd, sData, oData, iRow, iCol){
            var $temp = $($(nTd).html($.dtcheckboxbs4())).find("input[type='checkbox']");
            return $temp.attr("data-key","presentationContributionAllowed");
          }},
          {data: 't_seq', name: 'presentationViewingAllowed',fnCreatedCell:function(nTd, sData, oData, iRow, iCol){
            var $temp = $($(nTd).html($.dtcheckboxbs4())).find("input[type='checkbox']");
            return $temp.attr("data-key","presentationViewingAllowed");
          }},
          {data: 'devicetype', name:'devicetype'}
        ],
        columnDefs: [
          {targets: [0, 9, 10, 11, 12, 13, 14], orderable: 'false', searchable: false, checkboxes: true, className: "text-center text-middle"},
          {targets: [1, 2, 3, 4, 5, 6, 7, 8], className: "text-center text-middle"},
          {targets: [15], visible:false}
        ],
        initComplete: function () {
  
          var addbtn = $("<span>").addClass(["btn", "btn-outline", "b-primary", "text-primary", "m-r-2"])
                                  .text(gettext("버튼.공통.직접입력"))
                                  .on("click", function () {
                                    _mergeTableAdd();
                                  });
  
          var delbtn = $("<span>").addClass(["btn", "btn-outline", "b-danger", "text-danger", "m-r-2"])
                                  .text(gettext("버튼.공통.삭제"))
                                  .on("click", function () {
                                    _mergeTableDel();
                                  });
  
          var h5tag = $("<h5>").text(gettext("버튼.공통.참석자목록"));
  
          $(".tm-btn-group-merge").append(addbtn).append(delbtn);
          $(".tm-text-group-merge").append(h5tag);
  
        }
  
      }).columns.adjust();
  
      $(".table_merge > thead > tr > th > input[type='checkbox']").parent().html($.dtcheckboxbs4head());
  
      return _tableMerge;
  
    }
  
    // (PROMPT) Merge 테이블 ADD 버튼 이벤트
    function _mergeTableAdd() {
  
      var mergeData = $('#table_merge_filter.dataTables_filter input[type=search]').val();
      var mergeParamList = [];
      var mergeAddData = {};
          mergeAddData['t_seq'] = _mergeSeq;
          mergeAddData['ep_id'] = "";
          mergeAddData['name'] = "";
          mergeAddData['remoteParty'] = '';
          mergeAddData['bandwidth'] = _default_bandwidth;
          mergeAddData['ep_group_name'] = "";
          mergeAddData['devicetype'] = 'DIRECT';
  
      _mergeSeq = _mergeSeq + 1;
      mergeParamList.push(mergeAddData);
  
      _dataMerge(mergeParamList,true);
    }
  
    // Merge 테이블 DEL 버튼 이벤트
    function _mergeTableDel() {
  
      var mergeDelChkList = [];
      var mergeDelSelList = [];
      var mergeDelTableList = _tableMerge.column(0).checkboxes.selected();
  
      $.each(mergeDelTableList, function (key, value) {
        mergeDelChkList.push(value);
      });
  
      var mergeTableData = _tableMerge.rows().column(0).data();
  
      for (var j = 0; j < mergeDelChkList.length; j++) {
        for (var i = 0; i < mergeTableData.length; i++) {
          if (mergeTableData[i] == mergeDelChkList[j]) {
            mergeDelSelList.push(i);
            break;
          }
        }
      }
  
      for (var i = mergeDelSelList.length - 1; i >= 0; i--) {
        var mergeTempData = _tableMerge.row(mergeDelSelList[i]).data();
        if(mergeTempData['devicetype'] == "EP"){
          for(var j=_mergeEpList.length-1;j>=0;j--){
            if(mergeTempData['remoteParty'] == _mergeEpList[j]['remoteParty']){
              _mergeEpList.splice(j,1);
              break;
            }
          }
        }else if (mergeTempData['devicetype'] == "WEB"){
          for(var j=_mergeWebList.length-1;j>=0;j--){
            if(mergeTempData['remoteParty'] == _mergeWebList[j]['remoteParty']){
              _mergeWebList.splice(j,1);
              break;
            }
          }
        }
        _tableMerge.row(mergeDelSelList[i]).remove().draw();
      }
  
      // _tableEp 체크박스 해제
      for(var i=_tableEp.rows().data().length-1;i>=0;i--){
        var mergeTempFlag = true;
        for(var j=_mergeEpList.length-1;j>=0;j--){
          if(_tableEp.rows().data()[i]['callNumber'] == _mergeEpList[j]['remoteParty']){
            mergeTempFlag = false;
            break;
          }
        }
        if(mergeTempFlag){
          _tableEp.cell(i,0).checkboxes.deselect();
        }
      }
  
      // _tableWeb 체크박스 해제
      for(var i=_tableWeb.rows().data().length-1;i>=0;i--){
        
        var mergeTempFlag = true;
  
        for(var j=_mergeWebList.length-1;j>=0;j--){
          if(_tableWeb.rows().data()[i]['userJid'] == _mergeWebList[j]['remoteParty']){
            mergeTempFlag = false;
            break;
          }
        }
  
        if(mergeTempFlag){
          _tableWeb.cell(i,0).checkboxes.deselect();
        }
  
      }
  
    }
  
    // Merge 테이블 ROW 추가(중복 데이터 체크)
    function _dataMerge(data,directFlag) {
  
      var mergeTableData = _tableMerge.data();
  
      for (var i = 0; i < data.length; i++) {
        var mergeTempFlag = true;
        if(directFlag){
  
        }else{
          for (var j = 0; j < mergeTableData.length; j++) {
            if ((mergeTableData[j]['remoteParty'] == data[i]['remoteParty']) && (mergeTableData[j]['name'] == data[i]['name'])) {
              mergeTempFlag = false;
              break;
            }
          }
        }
        
        if (mergeTempFlag) {
          _tableMerge.row.add(data[i]).draw();
  
          // Share,View 체크박스 체크 이벤트
          var rowIdx = _tableMerge.rows()[0].length-1;
  
          if("undefined"!=typeof(data[i].presentationContributionAllowed)){
            if(data[i].presentationContributionAllowed == "Y"){
              _tableMerge.cell(rowIdx,"presentationContributionAllowed:name").checkboxes.select();
            }else{
              _tableMerge.cell(rowIdx,"presentationContributionAllowed:name").checkboxes.deselect();
            }
          }else{
            _tableMerge.cell(rowIdx,"presentationContributionAllowed:name").checkboxes.select();
          }
  
          if("undefined"!=typeof(data[i].presentationViewingAllowed)){
            if(data[i].presentationViewingAllowed == "Y"){
              _tableMerge.cell(rowIdx,"presentationViewingAllowed:name").checkboxes.select();
            }else{
              _tableMerge.cell(rowIdx,"presentationViewingAllowed:name").checkboxes.deselect();
            }
          }else{
            _tableMerge.cell(rowIdx,"presentationViewingAllowed:name").checkboxes.select();
          }
  
          if("undefined"!=typeof(data[i].txAudioMute)){
            if(data[i].txAudioMute == "Y"){
              _tableMerge.cell(rowIdx,"txAudioMute:name").checkboxes.select();
            }else{
              _tableMerge.cell(rowIdx,"txAudioMute:name").checkboxes.deselect();
            }
          }else{
            _tableMerge.cell(rowIdx,"txAudioMute:name").checkboxes.deselect();
          }
  
          if("undefined"!=typeof(data[i].rxAudioMute)){
            if(data[i].rxAudioMute == "Y"){
              _tableMerge.cell(rowIdx,"rxAudioMute:name").checkboxes.select();
            }else{
              _tableMerge.cell(rowIdx,"rxAudioMute:name").checkboxes.deselect();
            }
          }else{
            _tableMerge.cell(rowIdx,"rxAudioMute:name").checkboxes.deselect();
          }
  
          if("undefined"!=typeof(data[i].txVideoMute)){
            if(data[i].txVideoMute == "Y"){
              _tableMerge.cell(rowIdx,"txVideoMute:name").checkboxes.select();
            }else{
              _tableMerge.cell(rowIdx,"txVideoMute:name").checkboxes.deselect();
            }
          }else{
            _tableMerge.cell(rowIdx,"txVideoMute:name").checkboxes.deselect();
          }
  
          if("undefined"!=typeof(data[i].rxVideoMute)){
            if(data[i].rxVideoMute == "Y"){
              _tableMerge.cell(rowIdx,"rxVideoMute:name").checkboxes.select();
            }else{
              _tableMerge.cell(rowIdx,"rxVideoMute:name").checkboxes.deselect();
            }
          }else{
            _tableMerge.cell(rowIdx,"rxVideoMute:name").checkboxes.deselect();
          }
  
          _bindData(data[i]);
  
        }
      }
    }
  
    // Merge 테이블 데이터 제거
    function _mergeDataRemove(data){
      var mergeTableData = _tableMerge.data();
  
      // Step1. Merge 테이블 데이터 전체 For
      for(var i=mergeTableData.length-1;i>=0;i--){
        for(var j=0;j<data.length;j++){
          if(data[j]['devicetype'] == "EP"){ // endpoint 일 경우
            if(data[j]['callNumber'] == mergeTableData[i]['remoteParty']){
              _tableMerge.row(i).remove();
            }
          }
  
          if(data[j]['devicetype'] == "WEB"){ // WEBRTC 일 경우
            if(data[j]['userJid'] == mergeTableData[i]['remoteParty']){
              _tableMerge.row(i).remove();
            }
          }
  
        }
      }
  
      _tableMerge.draw();
    }
  
    // ---------------------------- WEBRTC ----------------------------
    $.fn.createWebrtcTable = function(option){
  
      var _this = $(this);
  
      _tableWeb = _this.DataTable({
        dom: '<"row"<"col-sm-6 tm-text-webrtc"f>""<"col-sm-6 tm-btn-webrtc text-right">">t<"row"<"col-sm-12"p>>',
        searching: false,
        paginate: true,
        pageLength: 5,
        processing: true,
        serverSide: true,
        ordering: false,
        ajax: {
          url: "/meetingroom/webrtc", //데이터를 가져올 url
          type: "POST",
          dataType: "json",
          data: function (d) {
            d.searchText = (typeof($("#webSearch").val())=="undefined") ? "" : $("#webSearch").val();
            d.csrfmiddlewaretoken = $('.hidden_csrftoken').val();
            d.group_seq= "0";
            d.server_seq= "0";
          },
          dataFilter: function (data) {
            var json = jQuery.parseJSON(data);
                json.recordsTotal = json.recordsTotal;
                json.recordsFiltered = json.recordsFiltered;
                json.data = json.user_list;
            return JSON.stringify(json);
          }
        },
        columns: [
          {data: "id", className:'text-center text-middle sel-check'},
          {data: "name"},
          {data: "email"},
          {data: "userJid"},
          {data: "tenant"}
        ],
        columnDefs: [
          {targets: 0, orderable: false, searchable: false, checkboxes: true, className: "text-center text-middle",fnCreatedCell:function(nTd, sData, oData, iRow, iCol){
            $(nTd).html($.dtcheckboxbs4());
          }},
          {targets: [1, 2, 3, 4], className: "text-center text-middle"}
        ],
        initComplete: function () {
  
          var searchBox = $("<input>").attr({"type":"text","id":"webSearch","placeholder":"Search"})
                                      .addClass(["form-control","dis-inline-block","m-r-2","tm-w-40"])
                                      .unbind()
                                      .bind('keyup',function(e){
                                        if (e.keyCode == 13) {
                                          _tableWeb.search(this.value).draw();
                                        }
                                      });
  
          // var searchBox = $("<input type='text' id='webSearch'>").addClass(["form-control","dis-inline-block","m-r-2"]).css("width","40%").attr("placeholder","Search");
          var h5tag = $("<h5>").text(gettext("common.invite.webrtclist"));
  
          $(".tm-btn-webrtc").append(searchBox);
          $(".tm-text-webrtc").append(h5tag);
  
          // 클릭 이벤트
          _webTableClickEvent(_this.find("thead"));
          
        },
        drawCallback:function(){
  
          // 클릭 이벤트
          _webTableClickEvent(_this.find("tbody"));
  
          // 체크박스 정리 이벤트
          for(var i=_tableWeb.rows().data().length-1;i>=0;i--){
            var webCheckFlag = true;
            for(var j=_mergeWebList.length-1;j>=0;j--){
              if(_tableWeb.rows().data()[i]['userJid'] == _mergeWebList[j]['remoteParty']){
                _tableWeb.cell(i,0).checkboxes.select();
                webCheckFlag = false;
                break;
              }
            }
            if(webCheckFlag){
              _tableWeb.cell(i,0).checkboxes.deselect();
            }
          }
  
        }
      }).columns.adjust();
  
      $(this).find("thead > tr > th > input[type='checkbox']").parent().html($.dtcheckboxbs4head());
  
      return _tableWeb;
  
    }
  
    // WebRTC 테이블 클릭 이벤트
    function _webTableClickEvent(ele){
      $(ele).find(".sel-check > label > input").each(function(){
        $(this).unbind().on("change",function(){
            var tempcheck = $(this).prop("checked");
            if(tempcheck){
              _webrtcTableAdd();
            }else{
              _webRtcTableCheckRemove();
            }
        });
      });
    }
  
    // WebRTC 테이블 ADD 버튼 이벤트
    function _webrtcTableAdd() {
  
      var webAddChkList = [];
      var webAddSelList = [];
      var webAddParamList = [];
      var webAddDataList = _tableWeb.column(0).checkboxes.selected();
  
      $.each(webAddDataList, function (key, value) {
        webAddChkList.push(value);
      });
  
      var webAddRowData = _tableWeb.rows().column(0).data();
  
      for (var j = 0; j < webAddChkList.length; j++) {
        for (var i = 0; i < webAddRowData.length; i++) {
          if (webAddRowData[i] == webAddChkList[j]) {
            webAddSelList.push(i);
            break;
          }
        }
      }
  
      for (var i = 0; i < webAddSelList.length; i++) {
  
        var webAddTableData = _tableWeb.row(webAddSelList[i]).data();
        var webAddData = {};
            webAddData['t_seq'] = _mergeSeq;
            webAddData['ep_id'] = "";
            webAddData['name'] = webAddTableData['name'];
            webAddData['remoteParty'] = webAddTableData['userJid'];
            webAddData['bandwidth'] = _default_bandwidth;
            webAddData['ep_group_name'] = "";
            webAddData['devicetype'] = 'WEB';
  
        _mergeSeq = _mergeSeq + 1;
  
        var tempFlag = true;
  
        for(var j=0;j<_mergeWebList.length;j++){
          if(_mergeWebList[j]['remoteParty'] == webAddData['remoteParty'] && _mergeWebList[j]['name'] == webAddData['name']){
            tempFlag = false;
            break;
          }
        }
  
        if(tempFlag){
          _mergeWebList.push(webAddData);
        }
  
        webAddParamList.push(webAddData);
  
      }
  
      _dataMerge(webAddParamList);
  
    }
  
    // WebRtc 테이블 체크박스 제거시 이벤트
    function _webRtcTableCheckRemove(){
  
      var webDelChkList = []; // 체크목록
      var webDelPageData = []; // 페이지 데이터
  
      // Step1. 해당 페이지 데이터 로드
      var webDelList = _tableWeb.column(0).checkboxes.selected();
  
      $.each(_tableWeb.rows().data(),function(){
        $(this)[0]['devicetype'] = "WEB";
        webDelPageData.push($(this)[0]);
      });
  
      // Step2. 체크 데이터 목록
      $.each(webDelList, function (key, value) {
        webDelChkList.push(value);
      });
  
      // Step3. 페이지 데이터 - 체크 데이터
      for(var i=webDelPageData.length-1;i >=0 ; i--){
        for(var j=0;j<webDelChkList.length;j++){
          if(webDelPageData[i]["id"] == webDelChkList[j]){
            webDelPageData.splice(i,1);
            break;
          }
        }
      }
  
      for(var i=_mergeWebList.length-1;i>=0;i--){
        for(var j=0;j<webDelPageData.length;j++){
          if(_mergeWebList[i]['remoteParty'] == webDelPageData[j]['userJid']){
            _mergeWebList.splice(i,1);
            break;
          }
        }
      }
  
      // Step4. Merge Table 데이터 삭제
      _mergeDataRemove(webDelPageData);
  
    }
  
    // ---------------------------- 공통 ----------------------------
    function _bindData(data){
      $(_tableMerge.row(_tableMerge.data().length - 1).node()).bindJsonToElement(data);
    }
  
    $.kotech.getMergeTableData = function(option){
  
      var _defaultOption = {}
      _defaultOption['dbFlag'] = false;
  
      if("undefined"!=typeof(option)){
        $.extend(true,_defaultOption,option);
      }
  
      var inviteList = [];
      var mergeList = _tableMerge.data();
  
      // var taList = _tableMerge.column("txAudioMute:name").checkboxes.selected();
      var taList = $('input[type="checkbox"][data-key="txAudioMute"]').map(function(){
        var temp = {};
        temp['txAudioMute'] = $(this).prop("checked");
        return temp;
      });
  
      // var raList = _tableMerge.column("rxAudioMute:name").checkboxes.selected();
      var raList = $('input[type="checkbox"][data-key="rxAudioMute"]').map(function(){
        var temp = {};
        temp['rxAudioMute'] = $(this).prop("checked");
        return temp;
      });
  
      // var tvList = _tableMerge.column("txVideoMute:name").checkboxes.selected();
      var tvList = $('input[type="checkbox"][data-key="txVideoMute"]').map(function(){
        var temp = {};
        temp['txVideoMute'] = $(this).prop("checked");
        return temp;
      });
  
      // var rvList = _tableMerge.column("rxVideoMute:name").checkboxes.selected();
      var rvList = $('input[type="checkbox"][data-key="rxVideoMute"]').map(function(){
        var temp = {};
        temp['rxVideoMute'] = $(this).prop("checked");
        return temp;
      });
  
      // var shareList = _tableMerge.column("presentationContributionAllowed:name").checkboxes.selected();
      var shareList = $('input[type="checkbox"][data-key="presentationContributionAllowed"]').map(function(){
        var temp = {};
        temp['presentationContributionAllowed'] = $(this).prop("checked");
        return temp;
      });
  
      // var viewList = _tableMerge.column("presentationViewingAllowed:name").checkboxes.selected();
      var viewList = $('input[type="checkbox"][data-key="presentationViewingAllowed"]').map(function(){
        var temp = {};
        temp['presentationViewingAllowed'] = $(this).prop("checked");
        return temp;
      });
  
      var remoteparty_list = $('input.remoteParty[type="text"]').map(function(){
        var temp = {};
        temp['remoteParty'] = $(this).val();
        return temp;
      }).get();
  
      var bw_list = $('select.bandwidth').map(function(){
        var temp = {};
        temp['bandwidth'] = $(this).val();
        return temp;
      }).get();
  
      var dtmf_list = $('input.dtmf[type="text"]').map(function(){
        var temp = {};
        temp['dtmf'] = $(this).val();
        return temp;
      }).get();
  
      var nlo_list = $('input.nameLabel[type="text"]').map(function(){
        var temp = {};
        temp['nameLabelOverride'] = $(this).val();
        return temp;
      }).get();
  
      var qm_list = $('select.qualityMain').map(function(){
        var temp = {};
        temp['qualityMain'] = $(this).find("option:selected").val();
        return temp;
      }).get();
  
      var qp_list = $('select.qualityPresentation').map(function(){
        var temp = {};
        temp['qualityPresentation'] = $(this).find("option:selected").val();
        return temp;
      }).get();
  
      for (var i = 0; i < mergeList.length; i++) {
  
        mergeData = mergeList[i];
        mergeData['rxAudioMute'] = _defaultOption['dbFlag'] == false ? "false":"N";
        mergeData['txAudioMute'] = _defaultOption['dbFlag'] == false ? "false":"N";
        mergeData['rxVideoMute'] = _defaultOption['dbFlag'] == false ? "false":"N";
        mergeData['txVideoMute'] = _defaultOption['dbFlag'] == false ? "false":"N";
        mergeData['presentationContributionAllowed'] = _defaultOption['dbFlag'] == false ? "false":"N";
        mergeData['presentationViewingAllowed'] = _defaultOption['dbFlag'] == false ? "false":"N";
  
        for(var j=0; j<raList.length;j++){
          if(i == j){          
            var tempFlag = raList[j]['rxAudioMute'];
            if(tempFlag){
              mergeData['rxAudioMute'] =  _defaultOption['dbFlag'] == false ? "true":"Y";
            }
            break;
          }
        }
  
        for(var j=0; j<taList.length;j++){
          if(i == j){
            var tempFlag = taList[j]['txAudioMute'];
            if(tempFlag){
              mergeData['txAudioMute'] =  _defaultOption['dbFlag'] == false ? "true":"Y";
            }
            break;
          }
        }
  
        for(var j=0; j<rvList.length;j++){
          if(i == j){
            var tempFlag = rvList[j]['rxVideoMute'];
            if(tempFlag){
              mergeData['rxVideoMute'] =  _defaultOption['dbFlag'] == false ? "true":"Y";
            }
            break;
          }
        }
  
        for(var j=0; j<tvList.length;j++){
          if(i == j){
            var tempFlag = tvList[j]['txVideoMute'];
            if(tempFlag){
              mergeData['txVideoMute'] =  _defaultOption['dbFlag'] == false ? "true":"Y";
            }
            break;
          }
        }
  
        for(var j=0; j<shareList.length;j++){
          if(i == j){
            var tempFlag = shareList[j]['presentationContributionAllowed'];
            if(tempFlag){
              mergeData['presentationContributionAllowed'] =  _defaultOption['dbFlag'] == false ? "true":"Y";
            }
            break;
          }
        }
  
        for(var j=0; j<viewList.length;j++){
          if(i == j){
            var tempFlag = viewList[j]['presentationViewingAllowed'];
            if(tempFlag){
              mergeData['presentationViewingAllowed'] =  _defaultOption['dbFlag'] == false ? "true":"Y";
            }
            break;
          }
        }
  
        inviteList.push(mergeData);
  
      }
  
      var temp = $.extend(true, inviteList, bw_list, dtmf_list, nlo_list, qm_list, qp_list, remoteparty_list);
      for(var i=temp.length-1;i>=0;i--){
        var remoteParty = temp[i]['remoteParty'];
        if(remoteParty == "" || typeof(remoteParty) == "undefined"){
          temp.splice(i,1);
        }
      }
      return temp;
  
    }
  
    function clearInviteTable(){
      _tableWeb.column().checkboxes.deselectAll();
      _tableEp.column().checkboxes.deselectAll();
      _tableMerge.column().checkboxes.deselectAll();
      _tableMerge.rows().remove().draw();
      _tableMerge.clear();
    }
  
    function pushWebList(data){
      _mergeWebList.push(data);
    }
  
    function pushEpList(data){
      _mergeEpList.push(data);
    }
  
    function clearWebList(){
      _mergeWebList = [];
    }
  
    function clearEpList(){
      _mergeEpList = [];
    }
  
    $.kotech.dataTable = {
      "dataMerge":_dataMerge,
      "clearInviteTable":clearInviteTable,
      "pushWebList":pushWebList,
      "pushEpList":pushEpList,
      "clearWebList":clearWebList,
      "clearEpList":clearEpList,
    }
  
  })(jQuery);
  