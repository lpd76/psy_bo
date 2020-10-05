/**
 * 
 */

$('#id_start_date').keyup(function(){
    /*if(/[0-9]{2}\:[0-9]{2}/.test($(this).val())){*/
        var startTime = $(this).val().split(' ');
        var endHours = parseInt(startTime[1].split(':')[0]) +1;
        endHours = Math.min(Math.max(endHours, 1), 24);
        $('#id_end_date').val(startTime[0]+' '+endHours +':'+ startTime[1]);
    /*}*/
});