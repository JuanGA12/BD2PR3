<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="7" justify="center" align="center">
        <v-form ref="form" v-model="valid" lazy-validation>
          <v-card elevation="10" color="blue lighten-3" style=" border-radius: 10px;">
            <v-container>
              <v-col cols="12" justify="center" align="center">
                <v-card color=#FAFAFA style=" border-radius: 15px;">
                  <v-container>
                    <v-file-input v-model="image" :rules="fileRules" :disabled="this.dis"
                      placeholder="Subir tu imagen"
                      label="Imagen"
                      prepend-icon="mdi-camera"
                      outlined
                      show-size
                      class="pa-3"
                      accept="image/*"
                      required>
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
                  </v-container>
                </v-card>
              </v-col>
              <v-col cols="5" justify="center" align="center">
                <v-card color=#FAFAFA style=" border-radius: 15px;">
                  <v-container>
                    <v-select v-model="Algoritmo" :items="Algoritmos" :rules="[v => !!v || 'Algoritmo es requerido']"
                      label="Algoritmo" required  placeholder="Escoge un algoritmo"
                      :disabled="this.dis"
                      >
                    </v-select>
                  </v-container>
                </v-card>
              </v-col>
            <v-col cols="4" v-if="Algoritmo == 'KNN-Sequential' || Algoritmo == 'KNN-Rtree'">
              <v-card color=#FAFAFA style=" border-radius: 15px;">
                <v-container>
                  <v-text-field :disabled="this.dis"
                    v-model="K"
                      :rules="[v => !!v || 'Valor de K requerido']"
                      label="Ingrese el valor de K"
                      required
                      placeholder="K"
                    >
                  </v-text-field>
                </v-container>
              </v-card>
            </v-col>
            <v-col cols="4" v-if="Algoritmo == 'Range Search-RTree'">
              <v-card color=#FAFAFA style=" border-radius: 15px;">
                <v-container>
                  <v-text-field :disabled="this.dis"
                    v-model="R"
                      :rules="[v => !!v || 'Valor del radio requerido']"
                      label="Ingrese el valor del radio"
                      required
                      placeholder="R"
                    >
                  </v-text-field>
                </v-container>
              </v-card>
            </v-col>
            <v-btn v-if="K > 0 || R > 0 " color="success" class="mr-4" :disabled="!valid" @click="cargar" justify="center" align="center">
              Realizar {{this.Algoritmo}}
            </v-btn>
            <v-btn v-if="K > 0  || R > 0 " color="error" class="mr-4" @click="reset">
              Limpiar formulario
            </v-btn >
            </v-container>
          </v-card>
        </v-form>
      </v-col>
      <v-col cols="12" v-if="Show == true && this.next == true">
        Resultado obtenido usando algoritmo {{this.Algoritmo}}
      </v-col>
    </v-row>
  </v-container>
</template>

<script>

export default {
  name: 'Home',
  data: ()=>({
    valid:true,
    dis:false,
    Show:false,
    image:[
    ],
    Algoritmos:[
      'KNN-Rtree',
      'KNN-Sequential',
      'Range Search-RTree'
    ],
    Algoritmo:'',
    K:'',
    R:'',
    fileRules: [
      v => !!v || 'Imagen requerida'
    ],
    response:{},
    next:false
  }),
  methods:{
    async cargar(){
      //console.log(this.image);
      const form = new FormData();
      form.append('file',this.image);
      form.append('Algoritmo',this.Algoritmo);
      form.append('K',this.K);
      form.append('R',this.R);

      if(this.K == ""){
        this.K = 0;
      }else{
        this.R = 0;
      }

      this.response = await this.$store.dispatch('Post_image',form);
      if(this.response.error){
        alert(this.response.error)
      }else{
        alert('Datos enviados correctamente')
        this.next = true;
      }  
      this.Show = true,
      this.dis = true,
      this.valid = false;
      console.log(this.response);
    
    },
    reset () {
      this.$refs.form.reset()
      this.Show = false,
      this.dis = false
      this.K = ''
      this.R = ''
    }
  }
}
</script>
