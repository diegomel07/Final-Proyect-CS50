function type_select(type)
{

    let input = document.querySelector('input');
        input.addEventListener('input', async function() {
            
            let response = await fetch(`/buscar_${type}?q=` + input.value);
            let animes = await response.text();
            document.querySelector('ul').innerHTML = animes;
        })

}