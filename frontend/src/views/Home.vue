<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" justify="center" alignn="center">
        <v-file-input v-model="image"
            placeholder="Subir tu Imagen"
            label="Imagen"
            prepend-icon="mdi-camera"
            outlined
            show-size
            class="pa-3"
            accept="image/*"
          >   
            <template v-slot:selection="{ text }">
              <v-chip
                small
                label
                color="primary"
              >
                {{ text }}  
              </v-chip>
            </template>
          </v-file-input>
        <v-btn @click="cargar">
          Enviar
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
// @ is an alias to /src
//import ml5 from 'ml5'

export default {
  name: 'Home',
  data: ()=>({
    image:[]
  }),
  methods:{
    cargar(){
      console.log(this.image);
    }
  }
}
</script>
