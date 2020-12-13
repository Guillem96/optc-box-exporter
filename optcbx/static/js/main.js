var currentScreenshotB64 = '';

$(document).ready(function () {

    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });

    $('#image-size-slider').change(function () {
        $('.slider-disp').html(`Image Size: ${this.value}x${this.value}`);
    })

    $('#screenshot-file').change(function () {
        console.log('New file detected');
        var file = this.files[0],
            reader = new FileReader();

        reader.onloadend = function () {
            var b64 = reader.result.replace(/^data:.+;base64,/, '');
            currentScreenshotB64 = b64;
            $("#export-btn").attr('disabled', false);
            $('.screenshot-preview').html(
                `<img class="img-fluid" 
                    alt="Character box screenshot" 
                    src="${reader.result}" 
                    style="margin: auto; display: block" 
                    width=200>`
            )
        };

        reader.readAsDataURL(file);
    });

    $('.loading-wrapper').hide();
});

function exportCharacterBox() {
    const imageSize = parseInt($('#image-size-slider').val());    
    const image = currentScreenshotB64;
    const body = {
        imageSize,
        image,
        returnThumbnails: true
    };

    console.log(imageSize);

    load();
    post('/export', body).then(renderExport);
}

function renderExport(response) {
    console.log(response)
    const n = response.characters.length;
    const characters = response.characters;
    const thumbnails = response.thumbnails;

    let table = `
        <table class="table table-hover">
            <thead>
                <tr>
                    <th scope="col">#</th>
                    <th scope="col">Thumbnail</th>
                    <th scope="col">Name</th>
                    <th scope="col">Actions</th>
                </tr>
        </thead>
        <tbody>`;
    for (let i = 0; i < n; i++) {
        const c = characters[i];
        const t = thumbnails[i];
        const url = "https://optc-db.github.io/characters/#/view/" + c.number;
        
        const actions = `
            <div id="${i}-actions" class="btn-group" role="group" aria-label="Basic example">
                <button id="${i}-ok"  onclick="updateFeed(${i}, 'ok')" "type="button" class="btn btn-outline-success"><i class="fas fa-smile-beam"></i></button>
                <button id="${i}-meh" onclick="updateFeed(${i}, 'meh')" type="button" class="btn btn-outline-warning"><i class="fas fa-meh"></i></button>
                <button id="${i}-bad" onclick="updateFeed(${i}, 'bad')" type="button" class="btn btn-outline-danger"><i class="fas fa-sad-tear"></i></button>
            </div>
        `;

        const row = `
            <tr>
                <th scope="row">${c.number}</th>
                <td><img src="${t}" class="img-fluid"></td>
                <td><a href="${url}">${c.name}</a></td>
                <td>${actions}</td>
            </tr>
        `;
        table += row;
    }
    table = table + `</tbody></table>`;
    $(".export-disp").html(table);
    endLoad();
}

function load() {
    $('.loading-wrapper').show();

    $('html, body').css({
        overflow: 'hidden',
        height: '100%'
    });
}

function endLoad() {
    $('.loading-wrapper').hide();

    $('html, body').css({
        overflow: 'auto',
        height: 'auto'
    });
}

function updateFeed(i, fb) {
    const colors = {
        ok: "text-success",
        meh: "text-warning",
        bad: "text-danger"
    }
    $('#' + i + '-actions').html(`<span class="${colors[fb]}"><b>Thanks!</b></span>`);
    post("/feedback", {fb}).then(function () { console.log("FB sent!"); });
}

function post(path, body) {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: path,
            type: "POST",
            data: JSON.stringify(body),
            contentType: "application/json",
            dataType: "json",
            success: data => resolve(data),
            error: console.err
        })
    });
}
