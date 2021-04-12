;(function ($) {

	//******************************************
	// SweetAlert2 7.x 버전대
	// 사용 Example (기본)
	// $.kotech.alert({
	//	"type":"info",                        // 타입종류 : error,warning,question,success,info
	//	"text":"common.label.delete",         // 텍스트
	//	"title":"common.label.info",          // 타이틀
	//  "error_detail" : false				  // tm_error 출력시
	//  "error_detail_message" : 에러내용     // tm_error 상세 내용
	//	"callback":function(isOK){            // 콜백펑션 (ok버튼 눌렀을때 후 작업)
	//
  //   }
	// })
	//******************************************
	$.kotech.alert = function(option){

		var defaultOption = {
			translate:true						//Text 관련 언어변경(gettext 펑션 적용), default : true
		}

		var mergeOption = {};
		var translateKey = ["title","text","titleText","confirmButtonText","cancelButtonText"];
		var orginalCallbackFn = null;
		var htmltext = null;
		var error_detail = typeof(option['error_detail']) == undefined ? false : typeof(option['error_detail']) == "undefined" ? false : true;

		if(error_detail){
			if(typeof(option.error_detail_message) != "undefined"){
				htmltext = "<br/><span class='detailErrorView hov-pointer'>상세보기</span>";
				htmltext += "<br><span class='deactive' style='font-size:14px;'>" + option.error_detail_message.replace(/(?:\r\n|\r|\n)/g, '<br />'); + "</span>";
			}
		}
		
		if("undefined"==typeof(option)){
			console.error("TMAlert:option not defined");
			return false;
		}

		if("undefined"==typeof(option['type'])){
			console.error("TMAlert:type not defined");
			return false;
		}

		option['type'] = option['type'].toLowerCase();

		switch(option['type']){
			case "info":
				defaultOption['title'] = "INFO";
				break;

			case "error":
				defaultOption['title'] = "ERROR";
				break;

			case "warning":
				defaultOption['title'] = "WARNING";
				break;

			case "question":
				defaultOption['title'] = "QUESTION";
				defaultOption['showCancelButton'] = true;
				defaultOption['confirmButtonText'] = '확인';
				defaultOption['cancelButtonText'] = '취소';
				defaultOption['allowOutsideClick'] = false;
				defaultOption['allowEscapeKey'] = false;
				break;

			case "success":
				defaultOption['title'] = "SUCCESS";
				break;

			default :
				console.error("TMAlert:Type Error");
				return false;
				break;
		}

		mergeOption = $.extend(true,defaultOption,option);

		orginalCallbackFn = mergeOption['callback'] || null;

		if(htmltext!=null){
			if(typeof(mergeOption['html'])!=null){
				mergeOption['html'] = mergeOption['html'] + htmltext;	
			}
		}

		if(mergeOption['translate']){
			for(var i=0;i<translateKey.length;i++){
				for (var key in mergeOption) {
					if(translateKey[i]==key){
						if(Array.isArray(mergeOption[key])){
							var tempList = [];
							var tempText = "";
							for(var i=0;i<mergeOption[key].length;i++){
								if(0==i){
									tempText = gettext(mergeOption[key][i]);
								}else{
									tempList.push(gettext(mergeOption[key][i]));
								}
							}

							mergeOption[key] = interpolate(tempText,tempList);
														
						}else{
							console.log("mergeOption[key] before result==>", mergeOption[key]);
							mergeOption[key] = gettext(mergeOption[key]);
							console.log("mergeOption[key] after result==>", mergeOption[key]);
						}
					}
				}
			}
		}

		delete mergeOption['translate'];
		delete mergeOption['callback'];
		delete mergeOption['error_detail'];
		delete mergeOption['error_detail_message'];

		try{
			Swal(mergeOption).then(orginalCallbackFn);

			if(error_detail){
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

		}catch(e){
			console.log(e);
		}

	}


})($);
