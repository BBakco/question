let $table = $('#table')
let $remove = $('#remove')
let selections = []

function getIdSelections() {
    return $.map($table.bootstrapTable('getSelections'), function (row) {
        return row.id
    })
}

function responseHandler(res) {
    $.each(res.rows, function (i, row) {
        row.state = $.inArray(row.id, selections) !== -1
    })
    return res
}

function operateFormatter(value, row, index) {
    return [
        '<a class="edit" href="javascript:void(0)" title="Like">',
        '<i class="fas fa-edit"></i>',
        '</a>  ',
        '<a class="remove" href="javascript:void(0)" title="Remove">',
        '<i class="fa fa-trash"></i>',
        '</a>'
    ].join('')
}

window.operateEvents = {
    'click .edit': function (e, value, row, index) {
        alert('You click edit action, row: ' + JSON.stringify(row))
    },
    'click .remove': function (e, value, row, index) {
        $table.bootstrapTable('remove', {
            field: 'id',
            values: [row.id]
        })
    }
}

function initTable() {
    $table.bootstrapTable('destroy').bootstrapTable({
        height: 600,
        locale: $('#locale').val(),
        columns: [{
                checkbox: true,
            },
            {
                field: 'id',
                title: 'E-mail',
                align: 'center',
                valign: 'middle',
                sortable: true,
            },
            {
                field: 'name',
                title: 'Name',
                align: 'center',
                sortable: true
            }, {
                field: 'price',
                title: 'Pass word',
                align: 'center',
            }, {
                field: '',
                title: 'Answer',
                align: 'center',
            }, {
                field: '',
                title: 'Question',
                align: 'center',
            }, {
                field: 'operate',
                title: 'Operate',
                align: 'center',
                clickToSelect: false,
                events: window.operateEvents,
                formatter: operateFormatter
            }
        ]

    })
    $table.on('check.bs.table uncheck.bs.table ' +
        'check-all.bs.table uncheck-all.bs.table',
        function () {
            $remove.prop('disabled', !$table.bootstrapTable('getSelections').length)

            // save your data, here just save the current page
            selections = getIdSelections()
            // push or splice the selections if you want to save all data selections
        })
    $table.on('all.bs.table', function (e, name, args) {
        console.log(name, args)
    })
    $remove.click(function () {
        let ids = getIdSelections()
        $table.bootstrapTable('remove', {
            field: 'id',
            values: ids
        })
        $remove.prop('disabled', true)
    })
}

$(function () {
    initTable()

    $('#locale').change(initTable)
})