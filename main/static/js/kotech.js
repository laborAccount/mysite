;(function ($) {

    $.kotech = {};
  
    $.fn.showInput = function (addParam) {
      var _this = this;
      var addClass = ["col-sm-4"];
      var changeClass = ["com-sm-8"];
      var addClassLen = 0;
      var defaultMainLen = 12;
      var prefixClass = "col-sm-";
  
      if ("undefined" != typeof(addParam) && Array.isArray(addParam)) {
        addClass = addParam;
      }
  
      for (var i = 0; i < addClass.length; i++) {
        if (-1 != addClass[i].indexOf("col-sm-")) {
          addClassLen = parseInt(addClass[i].substring(addClass[i].lastIndexOf("-") + 1));
          break;
        }
      }
  
      $(".tm-div").each(function () {
        var _ele = this;
        var classList = $(this).getClassList();
        var mainFlag = false;
  
        for (var i = 0; i < classList.length; i++) {
          if (classList[i] == "tm-main") {
            mainFlag = true;
          }
        }
  
        if (mainFlag) {
          for (var i = 0; i < classList.length; i++) {
            if (-1 != classList[i].indexOf("col-sm-")) {
              $(_ele).removeClass(classList[i]);
              break;
            }
          }
          $(_ele).addClass(prefixClass + (defaultMainLen - addClassLen));
        } else {
          $(_ele).addClass("deactive");
        }
  
      });
  
      _this.removeClass("deactive");
      for (var i = 0; i < addClass.length; i++) {
        _this.addClass(addClass[i]);
      }
  
      return this;
    }
  
    $.fn.hideInput = function () {
      var mainDiv = $(this)[0].previousElementSibling;
  
      $(mainDiv).removeClass("col-sm-8").addClass("col-sm-12");
      $(this).removeClass("col-sm-4").addClass("deactive");
    }
  
    // 선택한 요소 display 활성화 나머지는 deactive
    $.fn.showDiv = function () {
      var _ele = this;
  
      $(".tm-div").each(function () {
        var classList = $(this).getClassList();
        if ($(this)[0] == _ele[0]) {
          for (var i = 0; i < classList.length; i++) {
            if (-1 != classList[i].indexOf("col-sm-")) {
              $(this).removeClass(classList[i]);
              break;
            }
          }
          $(this).removeClass("deactive").addClass("col-sm-12")
        } else {
          for (var i = 0; i < classList.length; i++) {
            if (-1 != classList[i].indexOf("col-sm-")) {
              $(this).removeClass(classList[i]);
              break;
            }
          }
          $(this).addClass("deactive");
        }
      });
    }
  
    // 선택한 요소의 클래스 리스트 목록 추출
    $.fn.getClassList = function () {
      var classList = $(this[0]).attr("class").split(/\s+/);
      return classList;
    }
  
    // 선택요소 validation check
    $.fn.dataValidations = function() {
  
      var elements = $(this).find("[data-validation]");
      var returnValue = true;
  
      var _Validations, _Val, _Label;
  
      $(elements).each(function() {
          var tagName = this.tagName;
          _Validations = this.dataset.validation;
  
          switch(tagName) {
            case "P":
            case "SPAN":
              _Label = $('label[for="' + this.id + '"]').text();
              _Val = this.text;
              break;
            case "INPUT":
              var inputType = this.type;
              switch(inputType) {
                default:
                  _Label = $('label[for="' + this.id + '"]').text();
                  _Val = this.value;
                  break;
              }
              break;
            default:
              break;
          }
  
          if(!fnValidate(_Validations, _Val, _Label)) {
              returnValue = false;
              return false;
          }
      });
  
      if(!returnValue) {
        return false;
      }else{
        return true;
      }
  
    }
  
    function fnValidate (validations, val, label) {
  
      if(!validations) return false;
      if(!label) label = "";
      var alertTextArr = [];
      var alertText = "";
  
      var rtnValue = true;
      var validate = validations.split("|");
  
      for(var i=0; i<validate.length; i++) {
        rtnValue = true;
        var originValidations = validate[i];
        var validType, length;
  
        // length
        if(originValidations.indexOf("(") > 0) {
            validType = originValidations.substr(0, originValidations.indexOf("("));
            length = originValidations.substr(originValidations.indexOf("(")+1, originValidations.indexOf(")") - (originValidations.indexOf("(")+1));
            originValidations = validType;
        }
  
        switch(originValidations) {
          case "required":
            if(!val) {
                rtnValue = false;
                alertText = interpolate(gettext("common.alert.warning.required"), [label]);
            }
            break;
  
          case "maxlength":
            if(val.length > length) {
                rtnValue = false;
                alertText = interpolate(gettext("common.alert.warning.maxlength"), [label, length]);
            }
            break;
  
          case "minlength":
            if(val.length < length) {
              rtnValue = false;
              alertText = interpolate(gettext("경고.공통.최소길이"), [length , label]);
            }
  
            break;
  
          case "number":
  
            var result = (val == undefined || val == null || $.isNumeric(val));
  
            if(!result) {
                rtnValue = false;
                alertText = interpolate(gettext("common.alert.warning.number"), [label]);
            }
            break;
  
          case "plus":
            var result = (val == undefined || val == null || $.isNumeric(val));
  
            if(!result) {
                rtnValue = false;
                alertText = interpolate(gettext("common.alert.warning.number"), [label]);
            }else{
              if ( val <= 0 ){
                rtnValue = false;
                alertText = interpolate(gettext("common.alert.warning.plus"), [label]);
              }
            }
            break;
  
          case "minus":
            var result = (val == undefined || val == null || $.isNumeric(val));
  
            if(!result) {
                rtnValue = false;
                alertText = interpolate(gettext("common.alert.warning.number"), [label]);
            }else{
              if ( val >= 0 ){
                rtnValue = false;
                alertText = interpolate(gettext("common.alert.warning.minus"), [label]);
              }
            }
            break;
  
          case "ip":
            var regexp = /^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$/
            var result = regexp.test(val)
            
            if(!result) {
                rtnValue = false;
                alertText = interpolate(gettext("common.alert.warning.ip"), [label]);
            }
            break;
            
  
  
          default:
            break;
  
        }
  
        if(!rtnValue){
          fnWarningMessage(alertText);
          break;
        }
  
      }
  
      return rtnValue;
    }
  
    function fnWarningMessage(text) {
  
      $.kotech.alert({
        "type": "warning",
        "text": text
      });
  
      return false;
    }
  
    // 선택한 요소의 데이터 유효성 체크(data-required="true" 가 되있는 부분만)
    $.fn.dataValidation = function () {
      var elements = $(this).find("[data-required]");
      var ret = true;
      var radio_chk = false;
      var is_radio = false;
      var radio_text = "";
  
      $(elements).each(function () {
        var tempTagName = $(this)[0].tagName;
        var tempText = "";
  
        switch (tempTagName) {
  
          case "P":
          case "SPAN":
            if ("" == $(this).text()) {
              tempText = $('label[for="' + this.id + '"]').text();
              $.kotech.alert({
                "type": "warning",
                "text": ["common.alert.warning.missingvalue", tempText]
              });
              ret = false;
              return false;
            }
            break;
  
          case "INPUT":
            var tempType = $(this)[0].type;
            switch (tempType) {
              case "radio":
                is_radio = true;
                if (radio_text == "") {
                  radio_text = $('label[for="' + this.id + '"]').text();
                }
                if ($(this).is(":checked")) {
                  radio_chk = true;
                }
                break;
  
              default:
  
                if ("" == $(this).val()) {
                  tempText = $('label[for="' + this.id + '"]').text();
                  $.kotech.alert({
                    "type": "warning",
                    "text": ["common.alert.warning.missingvalue", tempText]
                  });
                  ret = false;
                  return false;
                }
                break;
            }
            break;
  
          default:
            break;
        }
  
        if (!ret) { //each 탈출
          return false;
        }
  
      });
  
      if (ret) {  // radio 체크
        if (is_radio) {
          if (!radio_chk) {
            $.kotech.alert({
              "type": "warning",
              "text": ["common.alert.warning.missingvalue", radio_text]
            });
            ret = false;
          }
        }
      }
      return ret;
    }
  
    // 선택한 요소의 데이터 Json 으로 받기 (attr 에 data-key="키이름" 인 항목만)
    $.fn.getElementByJson = function () {
  
      var elements = $(this).find("[data-key]");
      var returnJson = {};
  
      $(elements).each(function () {
        var tempTagName = $(this)[0].tagName;
  
        switch (tempTagName) {
  
          case "SPAN":
          case "P":
          case "DIV":
            returnJson[$(this).attr("data-key")] = $(this).text();
            break;
  
          case "SELECT":
            returnJson[$(this).attr("data-key")] = $(this).find("option:selected").val();
            break;
  
          case "INPUT":
            var tempType = $(this)[0].type;
            var tempDataKey = $(this).attr("data-key");
  
            switch (tempType) {
              case "radio":
                if ($(this).is(":checked")) returnJson[tempDataKey] = $(this).val();
                break;
  
              case "checkbox":
                returnJson[tempDataKey] = $(this).is(":checked");
                break;
  
              default:
                returnJson[tempDataKey] = $(this).val();
  
            }
            break;
  
          default:
  
        }
      });
  
      return returnJson;
    }
  
    // Json데이터 Element에 바인드
  
  
    $.fn.bindJsonToElement = function (data) {
      var elements = $(this).find("[data-key]");
      fn_bindJsonToElement(elements,data);
    }
  
    function fn_bindJsonToElement(elements,data){
  
      $.each(data, function (key, val) {
        if(typeof(val)=="object"){
          fn_bindJsonToElement(elements,data[key]);
        }else{
          $(elements).each(function () {
            if (key == $(this).attr("data-key")) {
  
              var tempTagName = $(this)[0].tagName;
              switch (tempTagName) {
  
                case "SPAN":
                case "P":
                case "DIV":
                  $(this).text(val);
                  break;
                case "SELECT":
                  $(this).find("option").each(function () {
                    if (val == $(this).val()) {
                      $(this).prop('selected', true);
                    }
                  })
                  break;
  
                case "INPUT":
                  var tempType = $(this)[0].type;
  
                  switch (tempType) {
                    case "radio":
                      (val == $(this).val()) ? $(this).prop('checked', true) : $(this).prop('checked', false);
                      break;
  
                    case "checkbox":
  
                      if(val){
                        if(typeof(val)=="string"){
                          (val=="True" || val=="true" || val==true || val=="Y")?$(this).prop('checked', true) : $(this).prop('checked', false);
                        }else if(typeof(val)=="boolean"){
                          val?$(this).prop('checked', true) : $(this).prop('checked', false);
                        }
                      }else{
                        $(this).prop('checked', false);
                      }
                      //val && (val=="true" || val==true) ? $(this).prop('checked', true) : $(this).prop('checked', false);
                      break;
  
                    default:
                      $(this).val(val);
  
                  }
                  break;
  
                default:
  
              }
            }
          });
        }
  
      });
    }
  
    
    // 해당 영역 value 값 초기화
    $.fn.dataClear = function () {
      var elements = $(this).find("[data-key]");
      $(elements).each(function () {
  
        var tempTagName = $(this)[0].tagName;
  
        switch (tempTagName) {
          case "SELECT":
            $(this).find('option:eq(0)').prop('selected', true);
            break;
  
          case "INPUT":
            var tempType = $(this)[0].type;
  
            switch (tempType) {
              case "radio":
                $(this).prop('checked', false);
                break;
  
              case "checkbox":
                $(this).prop('checked', false);
                break;
  
              default:
                $(this).val('');
  
            }
            break;
  
          default:
  
        }
  
      });
  
      return this;
    }
  
    function ajax_fn(option) {
  
      var defaultOption = {
        async: true,
        type: "POST",
        dataType: "text",
        useCover: true,
        callback: null,
        errConsole: false,
        includeCsrf : true,
        optClearInterval:false,
      }
  
      var mergeOption = $.extend(true, {}, defaultOption, option);
  
      if(mergeOption.includeCsrf){
        mergeOption.data.csrfmiddlewaretoken = $('.hidden_csrftoken').val();
      }
      
      var ajaxOption = {};
      ajaxOption = option;
  
      ajaxOption = $.extend(true,{},option,{
        async: mergeOption.async,
        data: mergeOption.data,
        type: mergeOption.type,
        url: mergeOption.url,
        beforeSend: function () {
          try {
            if (mergeOption.useCover) {
              $.kotech.showAjaxShadow();
            }
          } catch (e) {
            if (mergeOption.errConsole) {
              console.log(e);
            }
          }
        },
        success: function (data, textStatus, jqXHR) {
  
            var successFlag = true; // 정상 성공 여부
            var detailFlag = false; // Detail 보기 여부
            var alertType = "warning";
            var htmltext = "";
  
            if(data.result=="server_err"){ // 서버 에러 발생시
              
              htmltext = "서버 에러가 발생했습니다.<br>"+"(";
  
              if(typeof(data.error_message)!="undefined"){
                htmltext += ""+data.error_message;
              }else if(typeof(data.error) != "undefined"){
                htmltext += ""+data.error;
              }else if(typeof(data.tm_error) != "undefined"){
                htmltext += ""+data.tm_error;
              }
              htmltext += ")";
  
              if(typeof(data.tm_error_detail) != "undefined"){
                htmltext += "<br/><span class='detailErrorView hov-pointer'>상세보기</span>";
                htmltext += "<br><span class='deactive' style='font-size:14px;'>" + data.tm_error_detail.replace(/(?:\r\n|\r|\n)/g, '<br />'); + "</span>";
              }
  
              alertType = "error";
              successFlag = false;
              detailFlag = true;
  
            }else if(data.result=="server_warning"){ // 서버 프로세스중 경고
  
              htmltext = "요청 중 경고가 발생하였습니다.<br>"+"(";
  
              if(typeof(data.tm_warning)!="undefined"){
                htmltext += ""+data.tm_warning;
              }
  
              htmltext += ")";
  
              alertType = "warning";
              successFlag = false;
              detailFlag = false;
  
            }else if(data.result=="cisco_error"){ // 시스코 에러 발생시
  
              htmltext = "시스코 서버와 통신중 에러가 발생했습니다.<br>"+"(";
  
              if(typeof(data.cisco_error)!="undefined"){
                htmltext += ""+data.cisco_error;
              }
  
              htmltext += ")";
  
              alertType = "warning";
              successFlag = false;
              detailFlag = false;
              
            }else if(data.result=="cisco_list_error"){ // 시스코 여러 요청 처리중 에러 발생시
  
              htmltext = "시스코 서버와 통신중 에러가 발생했습니다(Multiple).<br>";
  
              if(typeof(data.cisco_list_error)!="undefined"){
                for(var i=0;i<data.cisco_list_error.length;i++){
                  htmltext += ""+data.cisco_list_error[i].cisco_error+"<br>";
                }
              }
  
              alertType = "warning";
              successFlag = false;
              detailFlag = false;
  
            }
  
            if(!successFlag){
  
              $.kotech.alert({
                type:alertType,
                html:htmltext
              });
  
              if(detailFlag){
  
                $(".detailErrorView").css("font-size","12px").unbind().on("click",function(){
                  if($(this).siblings("span").hasClass("deactive")){
                    $(this).siblings("span").removeClass("deactive").addClass('text-left float-l');
                    $(this).parent().parent().parent().addClass("tm-w-70");
                  }else{
                    $(this).siblings("span").addClass("deactive").removeClass("text-left float-l");
                    $(this).parent().parent().parent().removeClass("tm-w-70");
                  }
                });
  
              }
  
              return false;
            }
  
            if ("function" == typeof mergeOption.callback && null != mergeOption.callback) {
              mergeOption.callback(data);
            }
  
        },
        error: function (jqXHR, textStatus, errorThrown) {
          
          if(jqXHR.status == "403" || jqXHR.status == "401" ){
              for(let i=0;i<=100;i++){
                clearInterval(i);
              }
              $.kotech.alert({
                type:"warning",
                text:"common.session.fired",     // 세션이 만료되었습니다.
                callback:function(){
                  $.kotech.ajax({
                    url:"/logout",
                    data:{},
                    callback:function(data){
                      window.location = "/";
                    }
                  });
                }
              });
          }
  
          if(mergeOption.optClearInterval){
            for(i=0;i<999;i++){
              clearInterval(i);
            }
          }
  
          // if(jqXHR.status == "400" || || jqXHR.status == "404" || jqXHR.status == "500") {
          //   $.kotech.alert({
          //     type:"warning",
          //     text:"common.session.fired",     // 세션이 만료되었습니다.
          //     callback:function(){
          //       window.location.href = "/main";
          //     }
          //   });
          //
          // }
          // console.log("error");
        },
        complete: function (jqXHR, textStatus) {
  
          
  
          try {
            if (mergeOption.useCover) {
              $.kotech.hideAjaxShadow();
            }
          } catch (e) {
            if (mergeOption.errConsole) {
              console.log(e);
            }
          }
        }
      })
  
      return $.ajax(ajaxOption)
    };
  
    $.kotech.ajax = function (option) {
      ajax_fn(option);
    }
  
    $.dtcheckboxbs4head = function(option){
      var defaultClass = 'indigo';
      if(typeof(option)!="undefined"){
        defaultClass = option.toString();
      }
      var ele_label = $("<label>").addClass("md-check");
      var ele_input = $("<input>").attr("type","checkbox");
      var ele_i = $("<i>").addClass(defaultClass);
  
      ele_label.append(ele_input).append(ele_i);
  
      return ele_label;
    }
  
    $.dtcheckboxbs4 = function(option){
      var defaultClass = 'indigo';
      if(typeof(option)!="undefined"){
        defaultClass = option.toString();
      }
      var ele_label = $("<label>").addClass("md-check");
      var ele_input = $("<input>").attr("type","checkbox").addClass("dt-checkboxes")
      var ele_i = $("<i>").addClass(defaultClass);
  
      ele_label.append(ele_input).append(ele_i);
  
      return ele_label;
  
    }
  
    $.secToTime = function(sec){
  
        if("null"==sec || null==sec){
          return "00:00:00";
        }else{
          var fm = [
                Math.floor(sec / 60 / 60), // HOURS
                Math.floor(sec / 60) % 60, // MINUTES
                sec % 60 // SECONDS
          ];
          return $.map(fm, function(v, i) { return ((v < 10) ? '0' : '') + v; }).join(':');
        }
  
    }
  
    /* 
    * Form 데이터 보내기
    * obj = {
    *   method:"POST", (default : "POST")
    *   action:"/",
    *   target:"_blank" ( defulat : _blank) , (_blank,_self,_parent,_top)
    *   data:{
    *     "key":"value",
    *     "key2":"value2"
    *   }
    * }
    **/
    $.kotech.sendFormData = function(obj){
      fnSendFormData(obj);
    }
  
    function fnSendFormData(obj){
  
      var form = document.createElement('form');
      var methodList = ['post','get'];
      var methodFlag = true;
      var targetlist = ['_blank','_self','_parent','_top'];
  
      form.setAttribute('method', 'post');
      form.setAttribute('target', '_blank');
  
      // 메소드 타입 검사
      if(typeof(obj['method']) != "undefined"){
        for(var i=0;i<methodList.length;i++){
          if(obj['method'] === methodList[i]){
            methodFlag = true;
            form.setAttribute('method',obj['method']);
            break;
          }else{
            methodFlag = false;
          }
        }
      }
  
      if(!methodFlag){
        console.error("TMUtility sendFormData Error > Method Type");
        return false;
      }
  
      // target 검사
      if(typeof(obj['target'])!="undefined"){
        form.setAttribute('target',obj['target']);
      }
  
      // action 검사
      if(typeof(obj['action'])=="undefined"){
        console.error("TMUtility sendFormData Error > URL Not Input");
        return false;
      }else{
        form.setAttribute('action', obj['action']);
      }
  
      if(obj['data']!="undefined"){
  
        try{
          $.each(obj['data'],function(key,value){
            var tempObj = document.createElement('input');
            tempObj.setAttribute('type', 'hidden');
            tempObj.setAttribute('name', key);
            tempObj.setAttribute('value', value);
            form.appendChild(tempObj);
          });
  
        }catch (e){
          console.error("TMUtility sendFormData Error > " , e);
          return false;
        }
        
      }
  
      document.body.appendChild(form);
      form.submit();
  
    }
  
  })(jQuery);
  