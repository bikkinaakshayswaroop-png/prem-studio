document.addEventListener('DOMContentLoaded', function () {

    const calendarEl = document.getElementById('calendar');

    if (calendarEl) {

        const calendar = new FullCalendar.Calendar(calendarEl, {

            initialView: 'dayGridMonth',

            height: 700,

            selectable: true,
            dateClick: function(info) {

                const dateInput = document.getElementById("id_event_date");

    if(dateInput){

        dateInput.value = info.dateStr;

        dateInput.scrollIntoView({
            behavior: "smooth"
        });

    }

},

            events: '/booking-events/',

        });

        calendar.render();

    }

});