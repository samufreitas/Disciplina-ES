document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        locale: 'pt-br',
        plugins: ['interaction', 'dayGrid'],
        //defaultDate: '2019-04-12',
        //editable: true,
        eventLimit: true,
        events: 'eventos/',


        extraParams: function () {
            return {
                cachebuster: new Date().valueOf()
            };
        },
        eventClick: function(info) {
            info.jsEvent.preventDefault();

            // Obtém o ID do agendamento clicado
            var agendamentoId = info.event.id;

            // Solicita as informações do agendamento ao Django
            $.ajax({
                url: `/exibir_modal/${agendamentoId}/`, // Rota que retorna as informações do agendamento
                type: 'GET',
                dataType: 'json',
                success: function (data) {
                    // Preenche as informações no modal
                     // Sua string original
                    var tituloString = `${data.titulo}`;

                    // Dividir a string em palavras usando o espaço como delimitador
                    var pala = tituloString.split(' ');

                    // Remover a última palavra do array
                    var titulo = pala.pop();

                    // Criar uma nova string com todas as palavras, exceto a última
                    var tituloCompleto = pala.join(' ');

                    var minhaString = `${data.titulo}`;
                    // Dividir a string em palavras usando o espaço como delimitador
                    var palavras = minhaString.split(' ');

                    // Pegar a última palavra do array
                    var tipo = palavras[palavras.length - 1];

                    $('#title').text(`${tituloCompleto}.`);
                    $('#description').text(`${tipo}`);
                    $('#start').text(`${data.hora_inicio}.`);
                    $('#end').text(`${data.hora_fim}`);

                    // Abre o modal
                    $('#visualizar').modal('show');
                },
                error: function () {
                    // Lida com erros, se necessário
                }
            });
        }
    });

    calendar.render();
});