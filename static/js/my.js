/**
 * Created by yy on 15-3-10.
 */


//function jump(id,url){
//  $(id).load(url,function(){ $(id).fadeIn(500);}
//);}

/** zTree helper start  **/


/** zTree helper end  **/

function refresh_inform_tip_by_list(unread_list) {
    /**
     * 根据传入的[消息数目,通知数目]数组更新用户中心 inform 系列页面的新消息提醒
     */
    //unread_list = [get_unread_message_num(user),get_unread_notification_num(user)]
    var unread_message = $("#unread_message_num");
    var unread_notification = $("#unread_notification_num");
    if (unread_list[0] == 0)
        unread_message.hide();
    else {
        unread_message.show();
        unread_message.html(unread_list[0]);
    }
    if (unread_list[1] == 0)
        unread_notification.hide();
    else {
        unread_notification.show();
        unread_notification.html(unread_list[1]);
    }
    if (unread_list[0] == 0 && unread_list[1] == 0)
        $("#new_inform_label").hide();
    else
        $("#new_inform_label").show();
}

function refresh_inform_tip() {
    $.ajax({
        type: "POST",
        url: "{% url 'get_unread_json' %}",
        data: {},
        dataType: "json",
        success: function (data) {
            refresh_inform_tip_by_list(data)
        },
        error: function () {
        }
    })
}

function get_manage_selected_topics() {
    var result = [];
    $(".manager_cb").each(function () {
        if ($(this).prop("checked"))
            result.push($(this).val());
    });
    return result;
}

function manage_btn_action(url,btn_class_name) {
    var checked_topics_id_list = get_manage_selected_topics();
    if (checked_topics_id_list.length == 0)
        return false;
    //var url = btn.val();
    $.ajax({
        type: "POST",
        url: url,
        data: {"id_list": JSON.stringify(checked_topics_id_list), "forum_id": "{{ forum.id }}"},
        dataType: "json",
        success: function (data) {
            if (data.success)
                location.href = "{% url 'forum_index' bbs.name forum.tag %}";
            else
                alert(data.message);
        },
        error: function () {
            alert("信息提交失败");
        }
    });
}