let gridData = [];
let rows = 10;
let cols = 10;

$(document).ready(function() {
    for(let i=0; i<rows; i++) {
        let row = [];
        for(let j=0; j<cols; j++) {
            row.push(0);
            let item = $('<div>', { class: 'grid-item' });
            item.data('row', i);
            item.data('col', j);
            item.click(function() {
                $(this).toggleClass('selected');
                let row = $(this).data('row');
                let col = $(this).data('col');
                gridData[row][col] = gridData[row][col] === 0 ? 1 : 0;
            });
            $('#grid').append(item);
        }
        gridData.push(row);
        $('#grid').append($('<br>'));
    }
});

function saveImage() {
    $.ajax({
        url: '/update_grid',
        type: 'POST',
        data: JSON.stringify({grid: gridData}),
        contentType: 'application/json',
        success: function() {
            $.get('/save_image', function(data) {
                alert(`Image saved as ${data.filename}`);
            });
        }
    });
}

function saveImageWithBorder() {
    // Create a copy of the original grid data
    let gridDataWithBorder = JSON.parse(JSON.stringify(gridData));

    // Check for the border
    let bottomBorderExists = gridDataWithBorder[gridDataWithBorder.length-1].some(cell => cell === 1);
    let rightBorderExists = gridDataWithBorder.some(row => row[row.length-1] === 1);

    if (!bottomBorderExists) {
        // Remove the last row if it's empty
        gridDataWithBorder.pop();
    }

    if (!rightBorderExists) {
        // Remove the last column if it's empty
        for (let i = 0; i < gridDataWithBorder.length; i++) {
            gridDataWithBorder[i].pop();
        }
    }

    $.ajax({
        url: '/update_grid_with_border',
        type: 'POST',
        data: JSON.stringify({grid: gridDataWithBorder}),
        contentType: 'application/json',
        success: function() {
            $.get('/save_image_with_border', function(data) {
                alert(`Image saved with border as ${data.filename}`);
            });
        }
    });
}

