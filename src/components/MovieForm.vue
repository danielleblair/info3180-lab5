<template>
    <form @submit.prevent="saveMovie" method="post" id="movieForm">
        <h2>Add a Movie</h2>


        <div class="form-group mb-3">
            <label for="title" class="form-label"><b>Movie Title</b></label>
            <br>
            <input type="text" name="title" class="formcontrol" style="width: 600px;"/>
        </div>
        <div class="form-group mb-3">
            <label for="description" class="form-label"><b>Movie Description</b></label>
            <br>
            <textarea rows="5" cols="70" name="description" class="formcontrol"></textarea>
        </div>
        <div class="form-group mb-3">
            <label for="poster" class="form-label"><b>Movie Poster</b></label>
            <br>
            <input type="file" name="poster" class="formcontrol"/>
        </div>
        <div class="col-12">
            <button class="btn btn-primary" type="submit">Add Movie</button>
        </div>
    </form>
</template>

<script setup>

    import { ref, onMounted } from "vue";
    let csrf_token = ref("");

    const saveMovie=() => {

        let movieForm = document.getElementById('movieForm');
        let form_data = new FormData(movieForm);

        fetch("/api/v1/movies", {
            method: 'POST',
            body: form_data,
            headers: {
                'X-CSRFToken': csrf_token.value
            }
        })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            // display a success message
        })
        .catch(function (error) {
            console.log(error);
        });
    }

    function getCsrfToken() {
        fetch('/api/v1/csrf-token')
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            csrf_token.value = data.csrf_token;
    })
    }

    onMounted(() => {
        getCsrfToken();
    });



</script>

<style scoped>

form{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 20px;
}

#movieForm{
    display: block;
    padding: 30px;
}

.form-group{
    display: block;
}


</style>
