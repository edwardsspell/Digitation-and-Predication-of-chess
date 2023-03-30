package com.example.chess;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;

public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle icicle) {
        super.onCreate(icicle);
        setContentView(R.layout.activity_main);

        int SPLASH_DISPLAY_LENGTH = 3000;
        new Handler().postDelayed(() -> {
            Intent mainIntent = new Intent(MainActivity.this,camera.class);
            MainActivity.this.startActivity(mainIntent);
            MainActivity.this.finish();
        }, SPLASH_DISPLAY_LENGTH);
    }
}