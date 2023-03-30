package com.example.chess;

import android.app.AlertDialog;
import android.app.Dialog;
import android.content.Context;
import android.content.DialogInterface;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.EditText;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatDialogFragment;

public class IpPopup extends AppCompatDialogFragment {
    private EditText ip,port;
    private IpPopupListner listner;
    @NonNull
    @Override
    public Dialog onCreateDialog(@Nullable Bundle savedInstanceState) {
        AlertDialog.Builder builder = new AlertDialog.Builder(getActivity());
        LayoutInflater inflater = getActivity().getLayoutInflater();
        View view = inflater.inflate(R.layout.popup_dialogue,null);
        builder.setView(view).setTitle("IP Config").setNegativeButton("cancle", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {

            }
        }).setPositiveButton("ok", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                String Ip = ip.getText().toString();
                String Port = port.getText().toString();
                listner.applyText(Ip,Port);
            }
        });
        ip = view.findViewById(R.id.ip);
        port = view.findViewById(R.id.port);
        return builder.create();
    }

    @Override
    public void onAttach(@NonNull Context context) {
        super.onAttach(context);
        try {
            listner = (IpPopupListner) context;
        } catch (ClassCastException e) {
            throw  new ClassCastException(context.toString()+"Must Impliment IpPopupListner");
        }
    }

    public interface  IpPopupListner {
        void applyText(String Ip,String Port);
    }
}
