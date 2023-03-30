package com.example.chess;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.jetbrains.annotations.NotNull;

import java.io.IOException;
import java.util.concurrent.TimeUnit;

import no.bakkenbaeck.chessboardeditor.view.board.ChessBoardView;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.FormBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class chessper extends AppCompatActivity {

    ChessBoardView chessBoardView;
    RadioGroup radioGroup;
    RadioButton radioButton;
    Button predict;
    String fen,finalIp;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chessper);

        chessBoardView = findViewById(R.id.chessBoard);
        radioGroup = findViewById(R.id.radioGroup);
        predict = findViewById(R.id.button4);
        Intent intent = getIntent();
        fen = intent.getStringExtra("fen");
        finalIp = intent.getStringExtra("ip");
        chessBoardView.setFen(fen);
        fen = chessBoardView.getFen();

        predict.setOnClickListener(v -> {
            OkHttpClient okHttpClient = new OkHttpClient.Builder()
                    .connectTimeout(10, TimeUnit.SECONDS)
                    .writeTimeout(10, TimeUnit.SECONDS)
                    .readTimeout(30, TimeUnit.SECONDS)
                    .build();
            int radioId = radioGroup.getCheckedRadioButtonId();
            radioButton = findViewById(radioId);
            if(radioButton.getText().toString().equals("White")){
                fen = fen + " w";
            }
            else{
                fen = fen + " b";
            }
            RequestBody form = new FormBody.Builder().add("FEN",fen).build();
            Request request = new Request.Builder().url(finalIp+"predict").post(form).build();
            okHttpClient.newCall(request).enqueue(new Callback() {
                @Override
                public void onFailure(@NotNull Call call, @NotNull IOException e) {
                    runOnUiThread(() -> Toast.makeText(chessper.this,e.getMessage(),Toast.LENGTH_SHORT).show());

                }

                @Override
                public void onResponse(@NotNull Call call, @NotNull Response response) throws IOException {
                    fen = response.body().string();
                    chessBoardView.setFen(fen);
                }
            });
        });

    }
}