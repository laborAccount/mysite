

//main_chart
var init = new Date();
var initTime = ("0" + init.getHours()).slice(-2) + ":" + ("0" + init.getMinutes()).slice(-2) + ":" + ("0" + init.getSeconds()).slice(-2);

init.setTime(init.getTime() - 10000);
var initTimeMinus10 = ("0" + init.getHours()).slice(-2) + ":" + ("0" + init.getMinutes()).slice(-2) + ":" + ("0" + init.getSeconds()).slice(-2);

init.setTime(init.getTime() - 10000);
var initTimeMinus20 = ("0" + init.getHours()).slice(-2) + ":" + ("0" + init.getMinutes()).slice(-2) + ":" + ("0" + init.getSeconds()).slice(-2);

init.setTime(init.getTime() - 10000);
var initTimeMinus30 = ("0" + init.getHours()).slice(-2) + ":" + ("0" + init.getMinutes()).slice(-2) + ":" + ("0" + init.getSeconds()).slice(-2);

var queue = [initTimeMinus30, initTimeMinus20, initTimeMinus10, initTime];
var active_call_color = ['#FF0000','#0000FF','#00FF00','#FFFF00','#FF00FF','#00FFFF'];
var video_color = ['#FF0000','#0000FF','#00FF00','#FFFF00','#FF00FF','#00FFFF'];
var audio_color = ['#FF0000','#0000FF','#00FF00','#FFFF00','#FF00FF','#00FFFF'];
var activeCall = [];
var callLeg = [];
var audioBitRateOutgoing = [];
var audioBitRateIncoming = [];
var videoBitRateOutgoing = [];
var videoBitRateIncoming = [];

for(var i = 0 ; i< _server_list.length; i++){
    var activecall_ini = [0,0,0,0];
    var callLeg_ini = [0,0,0,0];
    var audioBitRateOutgoing_ini = [0,0,0,0];
    var audioBitRateIncoming_ini = [0,0,0,0];
    var videoBitRateOutgoing_ini = [0,0,0,0];
    var videoBitRateIncoming_ini = [0,0,0,0];
    activeCall.push(activecall_ini);
    callLeg.push(callLeg_ini);
    audioBitRateOutgoing.push(audioBitRateOutgoing_ini);
    audioBitRateIncoming.push(audioBitRateIncoming_ini);
    videoBitRateOutgoing.push(videoBitRateOutgoing_ini);
    videoBitRateIncoming.push(videoBitRateIncoming_ini);
}

var activeCallCanvas = document.getElementById('activeCall_Chart');
var callLegCanvas = document.getElementById('callLeg_Chart');
var videoOutCanvas = document.getElementById('videoOut_Chart');
var videoInCanvas = document.getElementById('videoIn_Chart');
var audioOutCanvas = document.getElementById('audioOut_Chart');
var audioInCanvas = document.getElementById('audioIn_Chart');

var activeCall_data = {
    labels: queue,
    datasets: []
};

var callLeg_data = {
    labels: queue,
    datasets: []
};

var videoOut_data = {
    labels: queue,
    datasets: []
};

var videoIn_data = {
    labels: queue,
    datasets: []
};

var audioOut_data = {
    labels: queue,
    datasets: []
};

var audioIn_data = {
    labels: queue,
    datasets: []
};

for(var i = 0 ; i< _server_list.length; i++){
    var label_data = {label: _server_list[i]['server_name'],borderColor: active_call_color[i],pointBackgroundColor:"#ffffff", backgroundColor: "rgba(98,132,243,0.3)",fill: 'start',data: [0, 0, 0, 0]};
    activeCall_data.datasets.push(label_data);

    label_data = {label: _server_list[i]['server_name'],borderColor: active_call_color[i],pointBackgroundColor:"#ffffff", backgroundColor: "rgba(98,132,243,0.3)",fill: 'start',data: [0, 0, 0, 0]};
    callLeg_data.datasets.push(label_data);

    label_data = {label: _server_list[i]['server_name'],borderColor: video_color[i],pointBackgroundColor:"#ffffff", backgroundColor: "rgba(98,132,243,0.3)",fill: 'start',data: [0, 0, 0, 0]};
    videoOut_data.datasets.push(label_data);

    label_data = {label: _server_list[i]['server_name'],borderColor: video_color[i],pointBackgroundColor:"#ffffff", backgroundColor: "rgba(98,132,243,0.3)",fill: 'start',data: [0, 0, 0, 0]};
    videoIn_data.datasets.push(label_data);

    label_data = {label: _server_list[i]['server_name'],borderColor: audio_color[i],pointBackgroundColor:"#ffffff", backgroundColor: "rgba(98,132,243,0.3)",fill: 'start',data: [0, 0, 0, 0]};
    audioOut_data.datasets.push(label_data);

    label_data = {label: _server_list[i]['server_name'],borderColor: audio_color[i],pointBackgroundColor:"#ffffff", backgroundColor: "rgba(98,132,243,0.3)",fill: 'start',data: [0, 0, 0, 0]};
    audioIn_data.datasets.push(label_data);
}

var option = {
    showLines: true,
    maintainAspectRatio: false,
    fill : "start",
    scales: {
        yAxes:  [{
                    display: true,
                    labelString: "Speed in Miles per Hour",
                    ticks: {
                        beginAtZero: true
                    },
                    scaleLabel: {
                        display: true,
                        labelString: "bit/s",
                        fontColor: "black"
                    }
                }]
    },
};

var option2 = {
    showLines: true,
    maintainAspectRatio: false,
    fill : "start",
    scales: {
        yAxes: [{
                display: true,
                fontColor: "green",
                ticks: {
                    beginAtZero: true,
                    stepSize : 5
                },
                scaleLabel: {
                    display: true,
                    labelString: "total",
                    fontColor: "black"
                }
        }]
    },
};

var activeCallChart = Chart.Line(activeCallCanvas,{
    data: activeCall_data,
    options: option2
});

var callLegChart = Chart.Line(callLegCanvas,{
  data: callLeg_data,
  options: option2
});

var videoOutChart = Chart.Line(videoOutCanvas,{
  data: videoOut_data,
  options: option
});

var videoInChart = Chart.Line(videoInCanvas,{
  data: videoIn_data,
  options: option
});

var audioOutChart = Chart.Line(audioOutCanvas,{
  data: audioOut_data,
  options: option
});

var audioInChart = Chart.Line(audioInCanvas,{
  data: audioIn_data,
  options: option
});

$(document).ready(function(){

    _page = new page();
    _page.init();

    function page(){

        this.init = function(){

            _page.init_read();
            _page.get_main_list();
            _page.listIntervalFunction();

        }

        // 처음 데이터 로드?
        this.init_read = function(){

            $.kotech.ajax({
                url:"/main/read",
                data:{},
                callback:function(data){

                    $('#limit_call').html(_settings.callLicense);
                    var listData = data.static_list;
                    var totConference = [];
                    var totCallLegs = [];
                    var labels = [];
            
                    for(var i=0;i<listData.length;i++){
                        totConference.push(listData[i].totConference);
                        totCallLegs.push(listData[i].totCallLegs);
                        labels.push(listData[i].MON);
                    }
            
                    var activeCallCanvas = document.getElementById('static_Chart');
                    var activeCall_data = {
                        labels: labels,
                        datasets: [
                            {
                                label: gettext('main.chart.meeting'),
                                borderColor: [
                                    'rgba(229,207,108,1)','rgba(249,235,170,1)','rgba(157,190,89,1)','rgba(212,229,181,1)','rgba(91,190,148,1)','rgba(182,228,209,1)',
                                    'rgba(88,132,179,1)','rgba(182,206,229,1)','rgba(204,102,134,1)','rgba(229,181,197,1)','rgba(230,133,112,1)','rgba(241,200,192,1)'
                                ],
                                backgroundColor: [
                                    "#E5CF6C","#F9EBAA","#9DBE59","#D4E5B5","#5BBE94","#B6E4D1",
                                    "#5884B3","#B6CEE5","#CC6686","#E5B5C5","#E68570","#F1C8C0"
                                ],
                                data: totConference
                            },
                            {
                                label: gettext('main.chart.calllegs'),
                                borderColor: "#6284f3",
                                pointBackgroundColor:"#ffffff",
                                backgroundColor: "rgba(98,132,243,0.0)",
                                data: totCallLegs,
                                type:'line'
                            }
                        ]
                    };
            
                    var option = {
                        showLines: true,
                        maintainAspectRatio: false,
                        fill : "start"
                    };
            
                    var activeCallChart = new Chart(activeCallCanvas,{
                        type : 'bar',
                        data: activeCall_data,
                        options: option
                    });
                }
        
            });

        }

        // 2번째 줄 데이터 로드
        this.get_main_list = function(){

            $.kotech.ajax({
                url:"/main/get_list",
                useCover:false,
                data:{},
                callback:function(data){

                    $('#meetingroom_total').text(data['total']);
                    $('#use_call_total').text(data['use_call']);
                    $('#cur_resv_total').text(data['cur_resv']);
                    $('#reservation_total').html('');
                    $('#reservation_total').html('Total Reservation '+data['total_resv'])
                    $('#resv_con_list').html('');
                    $('#activecall_list').html('');
                    $('#end_call_list').html('');
          
                    _page.createReserveList(data);
                    _page.createActiveCallList(data);
                    _page.createEndCallList(data);
                    _page.updateChartData(data['chart_data'])
                    
                }
            })
        }

        // 2번째 줄 데이터 로드 - 예약 목록
        this.createReserveList = function(data){

            for(var i = 0; i<data['resv_list'].length; i++){

                var _title = 'None';
                var _startdt = '';
                var _dot_flag = false;
                var last_div = null;

                if(data['resv_list'][i]['id'] != ''){
                    _title = data['resv_list'][i]['title'];
                    _startdt = data['resv_list'][i]['startdt'];
                    _dot_flag = true;
                }

                var a_tag = $('<a>').attr("href","/reserve").addClass("text-blue-grey1 txt").html('&nbsp;'+_title);
                var first_div =  $('<div>').css("display","inline-block").append(a_tag);
                var span_tag1 = $('<span>').addClass("sl-date text-muted").text(_startdt);
                var second_div = $('<div>').append(span_tag1,first_div);
                var third_div = $('<div>').addClass("sl_content dotted-items").append(second_div);
                if(_dot_flag){
                    last_div = $('<div>').addClass("sl-item b-blue-grey1 dotted-item").append(third_div);
                }else{
                    last_div = $('<div>').addClass("sl-item dotted-item").append(third_div);
                }
                
                $('#resv_con_list').append(last_div);

            }

        }

        // 2번째 줄 데이터 로드 - 진행중 회의 목록 로드
        this.createActiveCallList = function(data){
            for(var i = 0; i<data['call_list'].length; i++){
                
                if(data['call_list'][i]['@id'] != ''){
                    var call_date = _page.convertCallStartTime(data['call_list'][i]['durationSeconds']);
                    var a_tag = $('<a>').attr("href","#").attr('onclick',"javascript:_page.move_activecall_monitoring(this)").addClass("text-blue-grey2 txt")
                                                        .attr("data-group", data['call_list'][i]['group_seq'])
                                                        .attr("data-server", data['call_list'][i]['server_seq'])
                                                        .attr("data-calls", data['call_list'][i]['call_guid'])
                                                        .attr("data-cospace", data['call_list'][i]['cospace_guid'])
                                                        .html('&nbsp;'+data['call_list'][i]['name']);
                                                        
                    var first_div =  $('<div>').css("display","inline-block").append(a_tag);
                    var span_tag1 = $('<span>').addClass("sl-date text-muted conferenceStartTime").text(call_date);
                    var second_div = $('<div>').append(span_tag1,first_div);
                    var third_div = $('<div>').addClass("sl_content dotted-items").append(second_div);
                    var last_div = $('<div>').addClass("sl-item b-blue-grey2 dotted-item").append(third_div);
                    $('#activecall_list').append(last_div);
                }else{
                    var a_tag = $('<a>').attr("href","#").addClass("text-blue-grey2").text('None');
                    var first_div =  $('<div>').css("display","inline-block").append(a_tag);
                    var span_tag1 = $('<span>').addClass("sl-date text-muted");
                    var second_div = $('<div>').append(span_tag1,first_div);
                    var third_div = $('<div>').addClass("sl_content dotted-items").append(second_div);
                    var last_div = $('<div>').addClass("sl-item dotted-item").append(third_div);
                    $('#activecall_list').append(last_div);
                }
            }
        };

        // 2번째 줄 데이터 로드 - 예약 목록
        this.createEndCallList = function(data){
            for(var i = 0; i<data['endcall_list'].length; i++){
                if(data['endcall_list'][i]['call_id'] != ''){
                    var input_tag1 = $('<input>').attr('type','hidden').attr('data-field','call_id').val(data['endcall_list'][i]['callguid'])
                    var input_tag2 = $('<input>').attr('type','hidden').attr('data-field','cospace_id').val(data['endcall_list'][i]['cospaceguid'])
                    var first_div =  $('<div>').css("display","inline-block").append(input_tag1,input_tag2);
                    var span_tag2 = $('<a>').attr("href","/statics/meeting").addClass("text-blue-grey3 txt").html('&nbsp;'+data['endcall_list'][i]['callname']);
                    var call_end_time = data['endcall_list'][i]['callEndTime'];
                    var span_tag1 = $('<span>').addClass("sl-date text-muted").text(call_end_time.slice(0,-3));
                    var second_div = $('<div>').css("display","inline-block").append(span_tag2,first_div);
                    var third_div = $('<div>').addClass("sl_content dotted-items").append(span_tag1,second_div);
                    var last_div = $('<div>').addClass("sl-item  b-blue-grey3 dotted-item").append(third_div);
                    $('#end_call_list').append(last_div);
                }else{
                    var a_tag = $('<a>').attr("href","#").addClass("text-blue-grey3").text('None');
                    var first_div =  $('<div>').css("display","inline-block").append(a_tag);
                    var span_tag1 = $('<span>').addClass("sl-date text-muted");
                    var second_div = $('<div>').append(span_tag1,first_div);
                    var third_div = $('<div>').addClass("sl_content dotted-items").append(second_div);
                    var last_div = $('<div>').addClass("sl-item dotted-item").append(third_div);
                    $('#end_call_list').append(last_div);
                }
            }
        };

        // main list 인터벌
        this.listIntervalFunction = function(){
            setInterval(function(){
                _page.get_main_list();
            }, parseInt(_settings.main_list_timer));
        }


        this.updateChartData = function(data){

            var d = new Date();
            var currTime = ("0" + d.getHours()).slice(-2) + ":" + ("0" + d.getMinutes()).slice(-2) + ":" + ("0" + d.getSeconds()).slice(-2);

            queue.push(currTime);
            queue.shift();

            for(var i=0;i < data['error_call_list'].length;i++){

                Lobibox.notify("warning", {
                    'class': 'lobibox-error-info',
                    'title': 'Connection Error(Call)',
                    size: 'mini',
                    rounded: true,
                    delayIndicator: false,
                    sound:false,
                    msg: data['error_call_list'][i]['server_name'] + "<br>" + data['error_call_list'][i]['error'],
                    icon:true,
                    iconSource: 'fontAwesome',
                  });

            }

            for(var i=0;i < data['error_status_list'].length;i++){

                Lobibox.notify("warning", {
                    'class': 'lobibox-error-info',
                    'title': 'Connection Error(Status)',
                    size: 'mini',
                    rounded: true,
                    delayIndicator: false,
                    sound:false,
                    msg: data['error_call_list'][i]['server_name'] + "<br>" + data['error_call_list'][i]['error'],
                    icon:true,
                    iconSource: 'fontAwesome',
                  });

            }
    
            //callstatus
            var call_len = data['call_list'].length;

            for(var i = 0; i < call_len; i++){
                var tAC = 0;
                if(typeof(data['call_list'][i]['call_total']) != "undefined"){
                    tAC = Number(data['call_list'][i]['call_total']);
                }
                activeCall[i].push(tAC);
                activeCall[i].shift();
                activeCallChart.data.datasets[i]['data'] = activeCall[i];
            }

            var system_len = data['system_list'].length;
            for(var i = 0; i < system_len; i++){

                var tCA = 0;
                var tAO = 0;
                var tAI = 0;
                var tVO = 0;
                var tVI = 0;

                if(typeof(data['system_list'][i]['status']) != "undefined"){
                    var tempstatus = data['system_list'][i]['status'];
                    tCA = Number(tempstatus['callLegsActive']);
                    tAO = Number(tempstatus['audioBitRateOutgoing']);
                    tAI = Number(tempstatus['audioBitRateIncoming']);
                    tVO = Number(tempstatus['videoBitRateOutgoing']);
                    tVI = Number(tempstatus['videoBitRateIncoming']);
                }

                callLeg[i].push(tCA);
                callLeg[i].shift();
                callLegChart.data.datasets[i]['data'] = callLeg[i];

                audioBitRateOutgoing[i].push(tAO);
                audioBitRateOutgoing[i].shift();
                audioOutChart.data.datasets[i]['data'] = audioBitRateOutgoing[i];

                audioBitRateIncoming[i].push(tAI);
                audioBitRateIncoming[i].shift();
                audioInChart.data.datasets[i]['data'] = audioBitRateIncoming[i];

                videoBitRateOutgoing[i].push(tVO);
                videoBitRateOutgoing[i].shift();
                videoOutChart.data.datasets[i]['data'] = videoBitRateOutgoing[i];

                videoBitRateIncoming[i].push(tVI);
                videoBitRateIncoming[i].shift();
                videoInChart.data.datasets[i]['data'] = videoBitRateIncoming[i];
                
            }

            activeCallChart.update();
            callLegChart.update();
            audioOutChart.update();
            audioInChart.update();
            videoOutChart.update();
            videoInChart.update();
            
        }

        // 공통 Sec To Time 
        this.convertCallStartTime = function(sec){
            var nowD = new Date();
          
            if("null"==sec || null==sec){
              return "00:00:00";
            }else{
                var fm = [
                    Math.floor(sec / 60 / 60 / 24), // DAYS
                    Math.floor(sec / 60 / 60) % 24, // HOURS
                    Math.floor(sec / 60) % 60, // MINUTES
                    sec % 60 // SECONDS
                ];
          
                var retDate = new Date(nowD.getFullYear(),nowD.getMonth(),nowD.getDate()-fm[0],nowD.getHours()-fm[1],nowD.getMinutes()-fm[2]);
                return $.format.date(retDate,"yyyy-MM-dd HH:mm");
            }
        }    

        this.move_activecall_monitoring = function(data){

            var obj = {};
            var tempData = {};
            tempData['call_id'] = $(data).attr('data-calls');
            tempData['group_seq'] = $(data).attr('data-group');
            tempData['server_seq'] = $(data).attr('data-server');
            tempData['cospace_id'] = $(data).attr('data-cospace');
            tempData['csrfmiddlewaretoken'] = $('.hidden_csrftoken').val();

            obj['method'] = "post";
            obj['action'] = "/activecall_monitor";
            obj['target'] = "_self";
            obj['data'] = tempData;

            $.kotech.sendFormData(obj);
            
        }
          

    } // page

}); // document





